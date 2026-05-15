# Custom Marker Detector

This is a React Native Android application for Custom Visual Marker Detection.

## Setup Instructions

1. **Install Dependencies**
   ```bash
   npm install
   ```

2. **Run on Android**
   ```bash
   npx react-native run-android
   ```
   Or build the release APK:
   ```bash
   cd android
   ./gradlew assembleRelease
   ```

## Architecture
This app uses:
- `react-native-vision-camera` for low-latency camera access.
- `vision-camera-resize-plugin` for GPU hardware downscaling.
- `react-native-fast-opencv` for native C++ image processing via JSI bindings.
- `react-native-worklets-core` for running synchronous JS frame processors.

See `Approach.md` for a comprehensive technical breakdown of the detection and extraction logic.
"# Visual_Marker_detection" 
