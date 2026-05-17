import React, { useEffect, useState } from 'react';
import { StyleSheet, Text, View, Image, ScrollView, Dimensions, TouchableOpacity } from 'react-native';
import { Camera, useCameraDevice, useCameraPermission, useFrameProcessor } from 'react-native-vision-camera';
import { OpenCV, ObjectType, RotateFlags } from 'react-native-fast-opencv';
import { Worklets, useSharedValue } from 'react-native-worklets-core';
import { useResizePlugin } from 'vision-camera-resize-plugin';

export default function App() {
  const { hasPermission, requestPermission } = useCameraPermission();
  const device = useCameraDevice('back');
  const [markers, setMarkers] = useState<string[]>([]);
  const isProcessing = useSharedValue(false);
  const detectedCount = useSharedValue(0);
  const { resize } = useResizePlugin();

  useEffect(() => {
    if (!hasPermission) {
      requestPermission();
    }
  }, [hasPermission, requestPermission]);

  const addMarker = Worklets.createRunOnJS((base64: string) => {
    setMarkers(prev => {
      if (prev.length < 20) {
        return [...prev, base64];
      }
      return prev;
    });
  });

  const frameProcessor = useFrameProcessor((frame) => {
    'worklet';
    if (detectedCount.value >= 20 || isProcessing.value) {
      return;
    }
    
    isProcessing.value = true;
    
    try {
      // 1. Resize to a smaller, square-ish resolution for fast processing
      // We keep aspect ratio approximately or just force a 640x640 frame to avoid dealing with complex coordinate mapping.
      // But resize plugin requires aspect ratio to be similar, otherwise it stretches.
      // Let's just scale down by 4 for speed.
      const scaleDown = 4;
      const targetWidth = Math.floor(frame.width / scaleDown);
      const targetHeight = Math.floor(frame.height / scaleDown);
      
      const resized = resize(frame, { 
        scale: { width: targetWidth, height: targetHeight }, 
        pixelFormat: 'rgb' 
      });
      
      const mat = OpenCV.frameBufferToMat(targetHeight, targetWidth, resized);
      
      // 2. Grayscale
      const gray = OpenCV.createObject(ObjectType.Mat, 0, 0, 0);
      OpenCV.invoke('cvtColor', mat, gray, 7); // COLOR_RGB2GRAY = 7
      
      // 3. Threshold (Binary Inverse so black border becomes white contour)
      const thresh = OpenCV.createObject(ObjectType.Mat, 0, 0, 0);
      OpenCV.invoke('threshold', gray, thresh, 100, 255, 1); // THRESH_BINARY_INV = 1
      
      // 4. Find Contours
      const contours = OpenCV.createObject(ObjectType.PointVectorOfVectors, 0, 0, 0);
      const hierarchy = OpenCV.createObject(ObjectType.Mat, 0, 0, 0);
      OpenCV.invoke('findContoursWithHierarchy', thresh, contours, hierarchy, 0, 2); // RETR_EXTERNAL = 0, CHAIN_APPROX_SIMPLE = 2
      
      const contoursJS = OpenCV.toJSValue(contours);
      let bestSquare = null;
      let maxArea = 0;
      
      // Filter contours to find the marker border
      for (let i = 0; i < contoursJS.length; i++) {
        const contour = contoursJS[i];
        
        let area = 0;
        for (let j = 0; j < contour.length; j++) {
          const p1 = contour[j];
          const p2 = contour[(j + 1) % contour.length];
          area += p1.x * p2.y - p2.x * p1.y;
        }
        area = Math.abs(area) / 2;
        
        // A minimum area threshold (e.g. 1000 pixels in scaled frame)
        if (area > 1000 && area > maxArea) {
           maxArea = area;
           bestSquare = contour;
        }
      }
      
      if (bestSquare) {
        // Find 4 corners
        let tl = bestSquare[0], br = bestSquare[0];
        let tr = bestSquare[0], bl = bestSquare[0];
        let minSum = 100000, maxSum = -100000, minDiff = 100000, maxDiff = -100000;

        for (let i=0; i<bestSquare.length; i++) {
           const pt = bestSquare[i];
           const sum = pt.x + pt.y;
           const diff = pt.x - pt.y;
           if (sum < minSum) { minSum = sum; tl = pt; }
           if (sum > maxSum) { maxSum = sum; br = pt; }
           if (diff < minDiff) { minDiff = diff; bl = pt; } // Small x, large y -> min diff
           if (diff > maxDiff) { maxDiff = diff; tr = pt; } // Large x, small y -> max diff
        }

        const srcPoints = [tl, tr, bl, br];
        const srcVec = OpenCV.createObject(ObjectType.Point2fVector, srcPoints);
        
        const dstPoints = [
          {x: 0, y: 0},
          {x: 300, y: 0},
          {x: 0, y: 300},
          {x: 300, y: 300}
        ];
        const dstVec = OpenCV.createObject(ObjectType.Point2fVector, dstPoints);
        
        // Perspective Transform
        const M = OpenCV.invoke('getPerspectiveTransform', srcVec, dstVec, 0); // DECOMP_LU = 0
        const warped = OpenCV.createObject(ObjectType.Mat, 0, 0, 0);
        const size300 = OpenCV.createObject(ObjectType.Size, 300, 300);
        
        OpenCV.invoke('warpPerspective', gray, warped, M, size300, 1, 0, OpenCV.createObject(ObjectType.Scalar, 0)); // INTER_LINEAR=1, BORDER_CONSTANT=0
        
        // Check 4 corners of the inner white area (x=45 to 85, y=45 to 85, etc)
        const checkRegion = (x: number, y: number) => {
           const rect = OpenCV.createObject(ObjectType.Rect, x, y, 40, 40);
           const crop = OpenCV.createObject(ObjectType.Mat, 0, 0, 0);
           OpenCV.invoke('crop', warped, crop, rect);
           const meanColor = OpenCV.invoke('mean', crop);
           const meanVal = OpenCV.toJSValue(meanColor).val[0];
           return meanVal;
        };

        const tl_mean = checkRegion(45, 45);
        const tr_mean = checkRegion(215, 45);
        const bl_mean = checkRegion(45, 215);
        const br_mean = checkRegion(215, 215);

        // We expect exactly 1 dark region (the corner square) and 3 bright regions
        const threshold = 120; // darker than 120 is black, brighter is white
        let darkCount = 0;
        let darkCorner = -1;
        
        if (tl_mean < threshold) { darkCount++; darkCorner = 0; }
        if (tr_mean < threshold) { darkCount++; darkCorner = 1; }
        if (br_mean < threshold) { darkCount++; darkCorner = 2; }
        if (bl_mean < threshold) { darkCount++; darkCorner = 3; }

        if (darkCount === 1) {
           // We found the marker orientation!
           let finalWarped = warped;
           
           if (darkCorner !== 0) {
              finalWarped = OpenCV.createObject(ObjectType.Mat, 0, 0, 0);
              let rotateCode = RotateFlags.ROTATE_90_COUNTERCLOCKWISE; // 2
              if (darkCorner === 1) rotateCode = RotateFlags.ROTATE_90_COUNTERCLOCKWISE;
              else if (darkCorner === 2) rotateCode = RotateFlags.ROTATE_180; // 1
              else if (darkCorner === 3) rotateCode = RotateFlags.ROTATE_90_CLOCKWISE; // 0
              
              OpenCV.invoke('rotate', warped, finalWarped, rotateCode);
           }
           
           // Now check the center to ensure it's the correct marker and not the red X one.
           // The red X marker is mostly white in the center. The animal is dark (lots of edges/lines).
           // Center area: 100x100 at 100,100
           const centerRect = OpenCV.createObject(ObjectType.Rect, 100, 100, 100, 100);
           const centerCrop = OpenCV.createObject(ObjectType.Mat, 0, 0, 0);
           OpenCV.invoke('crop', finalWarped, centerCrop, centerRect);
           const centerMean = OpenCV.toJSValue(OpenCV.invoke('mean', centerCrop)).val[0];
           
           // If it's the empty one with Red X, center mean will be very high (e.g. > 240) since it's mostly white in grayscale.
           // If it's an animal, there are black lines, mean will be lower (e.g. < 230).
           if (centerMean < 235) {
              // Valid marker!
              // For the final output, let's extract from the colored Mat to look nice!
              const warpedColor = OpenCV.createObject(ObjectType.Mat, 0, 0, 0);
              OpenCV.invoke('warpPerspective', mat, warpedColor, M, size300, 1, 0, OpenCV.createObject(ObjectType.Scalar, 0));
              let finalColor = warpedColor;
              if (darkCorner !== 0) {
                 finalColor = OpenCV.createObject(ObjectType.Mat, 0, 0, 0);
                 let rotateCode = RotateFlags.ROTATE_90_COUNTERCLOCKWISE;
                 if (darkCorner === 1) rotateCode = RotateFlags.ROTATE_90_COUNTERCLOCKWISE;
                 else if (darkCorner === 2) rotateCode = RotateFlags.ROTATE_180;
                 else if (darkCorner === 3) rotateCode = RotateFlags.ROTATE_90_CLOCKWISE;
                 OpenCV.invoke('rotate', warpedColor, finalColor, rotateCode);
              }
              
              const b64 = OpenCV.toJSValue(finalColor).base64;
              detectedCount.value += 1;
              addMarker(b64);
           }
        }
      }
    } catch (e) {
      console.log('Error in frame processor', e);
    } finally {
      // Small throttle
      isProcessing.value = false;
    }
  }, [resize]);

  if (!device || !hasPermission) {
    return <View style={styles.container}><Text style={{color:'white'}}>No camera or permission</Text></View>;
  }

  return (
    <View style={styles.container}>
      <Camera
        style={StyleSheet.absoluteFill}
        device={device}
        isActive={markers.length < 20}
        frameProcessor={frameProcessor}
      />
      
      {markers.length < 20 && (
         <View style={styles.overlay}>
            <View style={styles.scanBox} />
            <Text style={styles.scanText}>Scanning... {markers.length}/20</Text>
         </View>
      )}

      {markers.length === 20 && (
        <View style={styles.resultsContainer}>
          <Text style={styles.resultsTitle}>Found 20 Markers!</Text>
          <ScrollView contentContainerStyle={styles.resultsContent}>
            {markers.map((m, i) => (
              <Image key={i} source={{ uri: `data:image/jpeg;base64,${m}` }} style={styles.markerImage} />
            ))}
          </ScrollView>
          <TouchableOpacity style={styles.resetBtn} onPress={() => { setMarkers([]); detectedCount.value = 0; }}>
             <Text style={styles.resetBtnText}>Scan Again</Text>
          </TouchableOpacity>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: 'black' },
  overlay: { ...StyleSheet.absoluteFillObject, justifyContent: 'center', alignItems: 'center' },
  scanBox: { width: 250, height: 250, borderWidth: 2, borderColor: '#00ff00', backgroundColor: 'transparent' },
  scanText: { color: '#00ff00', marginTop: 20, fontSize: 18, fontWeight: 'bold' },
  resultsContainer: { ...StyleSheet.absoluteFillObject, backgroundColor: 'rgba(0,0,0,0.9)', paddingTop: 50 },
  resultsTitle: { color: 'white', fontSize: 24, fontWeight: 'bold', textAlign: 'center', marginBottom: 20 },
  resultsContent: { flexDirection: 'row', flexWrap: 'wrap', padding: 10, justifyContent: 'center' },
  markerImage: { width: 300, height: 300, margin: 10, borderWidth: 2, borderColor: 'white' },
  resetBtn: { backgroundColor: '#00ff00', padding: 15, margin: 20, borderRadius: 10, alignItems: 'center' },
  resetBtnText: { color: 'black', fontSize: 18, fontWeight: 'bold' }
});
