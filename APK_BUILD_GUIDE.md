# APK Build & Distribution Guide

## Overview

This document provides multiple methods for obtaining or building the MarkerDetector APK file.

## Method 1: GitHub Actions (Recommended - Easiest)

The most straightforward approach is to use GitHub Actions for automated builds.

### Steps:

1. **Push code to GitHub**

   ```bash
   git push origin main
   ```

2. **Trigger build workflow**

   - Go to GitHub repository → Actions tab
   - Select "Build APK Release" workflow
   - Click "Run workflow"
   - Build completes automatically (5-10 minutes)

3. **Download APK**
   - Navigate to workflow run
   - Download "marker-detector-release" artifact
   - File: `MarkerDetector-release.apk`

### Configuration:

The workflow is defined in `.github/workflows/build-apk.yml` and includes:

- Automated SDK setup
- License acceptance
- Dependency installation
- Release build generation
- Artifact upload

## Method 2: Docker Build (Cross-Platform)

Build the APK in a Docker container without needing to install Android SDK locally.

### Prerequisites:

```bash
docker --version          # Docker 20.10+
docker-compose --version  # Docker Compose 1.29+
```

### Build Process:

```bash
# Option A: Using Docker directly
docker build -t marker-detector:builder .
docker run -v $(pwd)/android/app/build/outputs:/outputs marker-detector:builder

# Option B: Using Docker Compose (Recommended)
docker-compose up builder
```

### Result:

- APK location: `android/app/build/outputs/apk/release/app-release.apk`
- Filename: `MarkerDetector-release.apk`

### Docker Setup on Windows:

1. **Install Docker Desktop**: https://www.docker.com/products/docker-desktop
2. **Enable WSL 2** (Windows Subsystem for Linux)
3. **Run build**:
   ```bash
   docker-compose up builder
   ```

## Method 3: Local Build (Advanced)

If you have Android SDK properly configured locally.

### Prerequisites:

1. **Java Development Kit (JDK) 17+**

   ```bash
   java -version
   # Output should show version 17 or higher
   ```

2. **Android SDK Installation**

   - Download from: https://developer.android.com/studio/command-line-tools
   - Extract to: `C:\Android\sdk` (Windows) or `~/Android/sdk` (macOS/Linux)

3. **Set Environment Variables**

   **Windows (PowerShell):**

   ```powershell
   $env:ANDROID_HOME = "C:\Android\sdk"
   $env:ANDROID_SDK_ROOT = "C:\Android\sdk"
   $env:JAVA_HOME = "C:\Program Files\Java\jdk-17"
   ```

   **macOS/Linux (Bash):**

   ```bash
   export ANDROID_HOME=$HOME/Android/sdk
   export ANDROID_SDK_ROOT=$HOME/Android/sdk
   export JAVA_HOME=$(/usr/libexec/java_home -v 17)
   ```

4. **Install Android Components**

   ```bash
   sdkmanager --licenses  # Accept all licenses

   sdkmanager \
     "platforms;android-35" \
     "build-tools;35.0.0" \
     "ndk;27.1.12297006" \
     "platform-tools"
   ```

### Build Commands:

```bash
# Navigate to project
cd MarkerDetector/android

# Build release APK
./gradlew assembleRelease

# Output location:
# MarkerDetector/android/app/build/outputs/apk/release/app-release.apk
```

### Troubleshooting:

| Error                   | Solution                                                                   |
| ----------------------- | -------------------------------------------------------------------------- |
| "NDK not found"         | Run: `sdkmanager "ndk;27.1.12297006"`                                      |
| "Licenses not accepted" | Run: `sdkmanager --licenses` and accept all                                |
| "Java not found"        | Set `JAVA_HOME` environment variable                                       |
| "Gradle timeout"        | Increase memory: Add `org.gradle.jvmargs=-Xmx4096m` to `gradle.properties` |

## Method 4: Pre-Built Release (If Available)

Check GitHub Releases for pre-built APK files:

1. Go to: `https://github.com/[username]/marker-detector/releases`
2. Download latest `MarkerDetector-release.apk`
3. Install on device (see Installation section below)

## Installation on Android Device

### Via ADB (Android Debug Bridge):

```bash
# Connect device via USB or emulator running
adb install -r MarkerDetector-release.apk

# Verify installation
adb shell pm list packages | grep markerdetector
```

### Via Direct File:

1. Copy `MarkerDetector-release.apk` to device
2. Open file manager on device
3. Tap APK file to install
4. Grant permissions when prompted

### Enable Installation from Unknown Sources (if needed):

1. Settings → Security → Unknown Sources
2. Toggle ON for your security app or file manager
3. Retry installation

## Build Output Structure

```
MarkerDetector/
├── android/
│   └── app/
│       └── build/
│           └── outputs/
│               └── apk/
│                   ├── debug/
│                   │   └── app-debug.apk          (For testing)
│                   └── release/
│                       └── app-release.apk        (Production build)
```

## Signing Information

### Debug Build:

- **Keystore**: `android/app/debug.keystore`
- **Password**: `android`
- **Key Alias**: `androiddebugkey`
- **Valid For**: Development and testing

### Release Build:

Currently uses debug keystore for expedited development. For production release:

1. Generate production keystore:

   ```bash
   keytool -genkey -v -keystore my-release-key.keystore \
     -keyalg RSA -keysize 2048 -validity 10000 \
     -alias my-key-alias
   ```

2. Update `android/app/build.gradle`:
   ```gradle
   signingConfigs {
       release {
           storeFile file("path/to/my-release-key.keystore")
           storePassword "your-keystore-password"
           keyAlias "my-key-alias"
           keyPassword "your-key-password"
       }
   }
   ```

## Continuous Integration Setup

### GitHub Actions (Already Configured)

The repository includes automated CI/CD pipeline in `.github/workflows/build-apk.yml` that:

- Builds on every push to main
- Runs on pull requests
- Creates releases on version tags (v1.0.0, etc.)
- Uploads APK as artifact for 30 days

### Environment Secrets (For Releases):

If uploading to Play Store, add these secrets to GitHub:

- `ANDROID_KEYSTORE`: Base64-encoded keystore file
- `KEYSTORE_PASSWORD`: Keystore password
- `KEY_ALIAS`: Key alias name
- `KEY_PASSWORD`: Key password

## Deployment Channels

### Beta Testing:

- Use debug APK for quick testing
- Share via GitHub actions artifacts
- Test on multiple devices

### Production Release:

- Use release APK signed with production keystore
- Upload to Google Play Store
- Consider Firebase App Distribution for beta programs

## Size & Performance Notes

| Metric             | Value                         |
| ------------------ | ----------------------------- |
| APK Size (Release) | ~45-55 MB                     |
| Installation Size  | ~80-100 MB (with native libs) |
| Minimum Android    | API 24 (Android 7.0)          |
| Target Android     | API 35 (Android 15)           |
| Tested Devices     | 6GB+ RAM recommended          |

## Cleanup Commands

```bash
# Clean build artifacts
cd android && ./gradlew clean

# Clear Gradle cache
rm -rf ~/.gradle/caches

# Clear Android build cache
rm -rf android/app/build

# Full clean rebuild
./gradlew clean && ./gradlew assembleRelease
```

## Advanced Build Customization

### Custom Build Variants:

Edit `android/app/build.gradle`:

```gradle
productFlavors {
    dev {
        applicationIdSuffix ".dev"
        versionNameSuffix "-dev"
    }
    staging {
        applicationIdSuffix ".staging"
    }
    prod {
        // Production defaults
    }
}
```

Build specific variant:

```bash
./gradlew assembleDevRelease
./gradlew assembleStagingRelease
./gradlew assembleProdRelease
```

### Performance Profiling:

```bash
# Build with profiling
./gradlew assembleRelease --profile

# View profiling report
cat build/reports/profile/profile-*.html
```

## Common Issues & Solutions

### Out of Memory:

```bash
# Increase Gradle heap
export GRADLE_OPTS="-Xmx4g"
./gradlew assembleRelease
```

### Slow Build:

```bash
# Parallel build
./gradlew assembleRelease --parallel

# Daemon build
./gradlew assembleRelease --daemon

# Skip tests
./gradlew assembleRelease -x test
```

### NDK Issues:

```bash
# Verify NDK installation
ls $ANDROID_HOME/ndk/27.1.12297006

# Force rebuild
./gradlew clean assembleRelease -x lint
```

---

**Last Updated**: May 2026  
**Version**: 1.0.0  
**For Questions**: See README.md and BUILD_SETUP.md
