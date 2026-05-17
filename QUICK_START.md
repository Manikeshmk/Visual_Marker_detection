# Quick Start Guide - Custom Marker Detector

**Get started in 5 minutes!**

---

## Option 1: Try It Immediately (No Installation)

### 1. Download Pre-Built APK (If Available)

- Visit: GitHub Releases
- Download: `MarkerDetector-release.apk`
- Install: `adb install -r MarkerDetector-release.apk`
- Run: Open app on Android device, grant camera permission

---

## Option 2: Build & Run (15 minutes)

### Prerequisites Checklist:

```
✓ Android device or emulator
✓ Node.js 18+ installed
✓ Android SDK API 35+
```

### Step-by-Step:

#### 1. Install Project Dependencies

```bash
cd MarkerDetector
npm install
```

#### 2. Build APK

```bash
# Option A: Using GitHub Actions (Easiest - No local setup)
# Push to GitHub, Actions builds automatically

# Option B: Using Docker (Recommended)
docker-compose up builder

# Option C: Local build (Requires Android SDK setup)
cd android
./gradlew assembleRelease
cd ..
```

#### 3. Install on Device

```bash
adb install -r android/app/build/outputs/apk/release/app-release.apk
```

#### 4. Run Application

- Open app on device
- Grant camera permission
- Point camera at markers
- Collect 20 markers

---

## Option 3: Develop Locally (20 minutes)

### 1. Full Project Setup

```bash
# Clone
git clone https://github.com/[username]/marker-detector.git
cd marker-detector

# Install dependencies
npm install

# Set up Android SDK (if needed)
# Follow BUILD_SETUP.md
```

### 2. Start Development Server

```bash
npm start
```

### 3. Run on Android

```bash
# In another terminal
npx react-native run-android

# Or install manually
cd android
./gradlew installDebug
cd ..
adb shell am start -n com.markerdetector/.MainActivity
```

### 4. Make Changes

- Edit `App.tsx`
- Save and hot reload (Reload JS in device menu)
- Test changes immediately

---

## Testing the App

### With Test Markers:

```bash
# Generate test marker images
python generate_test_markers.py

# Test images created in test-images/
# Use on computer display or print them
```

### Validation:

1. ✓ Should detect all correct markers (dog, cat, bird)
2. ✓ Should reject incorrect markers (red X, no corner, blank)
3. ✓ Should work in all orientations (0°, 90°, 180°, 270°)
4. ✓ Should show 25+ FPS frame rate

---

## Project Layout

```
Key Files:
├── App.tsx ..................... Main app code (270 lines)
├── README.md ................... Complete user guide
├── Approach.md ................. Architecture overview
├── TECHNICAL_APPROACH.pdf ...... Detailed technical docs
├── BUILD_SETUP.md .............. Android build setup
├── APK_BUILD_GUIDE.md .......... Build methods & troubleshooting
├── MARKER_GENERATION.md ........ Create custom markers
├── test-images/ ............... Test marker images (9 total)
└── android/ ................... Android build files
```

---

## Common Tasks

### Build for Testing

```bash
# Debug APK (faster, larger)
cd android && ./gradlew assembleDebug && cd ..

# Install & run
adb install -r android/app/build/outputs/apk/debug/app-debug.apk
adb shell am start -n com.markerdetector/.MainActivity
```

### Build for Release

```bash
# Release APK (smaller, slower to build)
cd android && ./gradlew assembleRelease && cd ..

# APK location:
# android/app/build/outputs/apk/release/app-release.apk
```

### Create Custom Markers

```python
# Edit or use generate_test_markers.py as template
python generate_test_markers.py
```

### Troubleshoot Issues

```bash
# Check logs
adb logcat | grep MarkerDetector

# Clear app data
adb shell pm clear com.markerdetector

# Reinstall completely
adb uninstall com.markerdetector
adb install -r [apk-path]
```

---

## Performance Expectations

| Metric         | Expected       | Notes                |
| -------------- | -------------- | -------------------- |
| Startup Time   | 2-5 sec        | First app launch     |
| Detection Time | 10-20 ms/frame | Per-frame processing |
| Batch Time     | 2700 ms        | All 20 markers       |
| Frame Rate     | 25-30 FPS      | Camera stream        |
| Memory         | 100-150 MB     | During use           |

---

## Next Steps

1. **Try the app** - Use pre-built APK or build locally
2. **Read documentation**:
   - README.md for general info
   - TECHNICAL_APPROACH.pdf for details
   - Approach.md for architecture
3. **Test thoroughly** - Use provided test markers
4. **Customize** - Modify App.tsx for your use case
5. **Deploy** - Push APK to device or Play Store

---

## File Sizes

```
APK (Debug):    ~50 MB
APK (Release):  ~45 MB
Installed:      ~100 MB (with native libraries)
Test Markers:   ~50 KB total (9 PNG files)
```

---

## Supported Devices

- **Minimum**: Android 7.0 (API 24)
- **Target**: Android 15 (API 35)
- **RAM**: 2GB minimum, 6GB recommended
- **Camera**: Rear-facing camera required
- **Processing**: Any modern processor

---

## Troubleshooting

### App crashes on startup

```bash
adb logcat | grep FATAL  # Check error logs
adb shell pm grant com.markerdetector android.permission.CAMERA  # Grant permission
```

### Markers not detected

- Ensure good lighting
- Markers should be clear and in focus
- Try different distances (30cm - 2m)
- Check if orientation square (black corner) is present

### Build fails

- See BUILD_SETUP.md for SDK setup
- See APK_BUILD_GUIDE.md for troubleshooting
- Try: `./gradlew clean` then rebuild

### Low frame rate

- Close other apps
- Reduce background tasks
- Check device temperature

---

## Key Documentation

| Document               | For               | Read Time |
| ---------------------- | ----------------- | --------- |
| README.md              | General users     | 5 min     |
| TECHNICAL_APPROACH.pdf | Technical details | 30 min    |
| APK_BUILD_GUIDE.md     | Building app      | 10 min    |
| BUILD_SETUP.md         | Android setup     | 15 min    |
| MARKER_GENERATION.md   | Custom markers    | 10 min    |

---

## Support Resources

1. **Installation Problems**: BUILD_SETUP.md
2. **Build Issues**: APK_BUILD_GUIDE.md
3. **How It Works**: TECHNICAL_APPROACH.pdf
4. **Using the App**: README.md
5. **Making Markers**: MARKER_GENERATION.md

---

## Version Info

- **App Version**: 1.0.0
- **React Native**: 0.79.2
- **Last Updated**: May 2026
- **Status**: Production Ready ✓

---

**Ready to go! Pick an option above and get started!**
