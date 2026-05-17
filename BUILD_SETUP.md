# Android Build Setup Guide

## Prerequisites

1. **Java Development Kit (JDK) 17+**
   - Already installed: OpenJDK 25.0.2
2. **Android SDK**

   - Download from: https://developer.android.com/studio/command-line-tools
   - Install to: `D:\react_native\`

3. **Install Required SDK Components**

   ```bash
   cd D:\react_native\cmdline-tools\latest\bin

   # Accept all licenses
   .\sdkmanager.bat --licenses

   # Install required components
   .\sdkmanager.bat "platforms;android-35"
   .\sdkmanager.bat "build-tools;35.0.0"
   .\sdkmanager.bat "ndk;27.1.12297006"
   .\sdkmanager.bat "platform-tools"
   .\sdkmanager.bat "cmdline-tools;latest"
   ```

## Build Instructions

### Option 1: Using Gradle (Recommended)

```bash
cd MarkerDetector\android
.\gradlew.bat assembleRelease
```

The signed APK will be located at:
`MarkerDetector\android\app\build\outputs\apk\release\app-release.apk`

### Option 2: Using React Native CLI

```bash
cd MarkerDetector
npx react-native run-android
```

### Option 3: Using Docker (If local setup fails)

```bash
docker build -t marker-detector-build .
docker run -v %cd%\android\app\build\outputs:/app/outputs marker-detector-build
```

## Troubleshooting

### "NDK not found" Error

- Ensure NDK 27.1.12297006 is installed via sdkmanager
- Verify `local.properties` has correct paths

### "License not accepted" Error

- Run: `.\sdkmanager.bat --licenses` and accept all when prompted

### Out of Memory

- Modify `android/gradle.properties`:
  ```
  org.gradle.jvmargs=-Xmx4096m -XX:MaxMetaspaceSize=512m
  ```

## Environment Variables

Set these before building:

```powershell
$env:ANDROID_SDK_ROOT = "D:\react_native"
$env:ANDROID_HOME = "D:\react_native"
$env:JAVA_HOME = "C:\Program Files\Java\temurin-25"
```
