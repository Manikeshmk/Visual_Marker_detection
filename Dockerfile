FROM ubuntu:22.04

# Set environment variables
ENV ANDROID_HOME=/android-sdk \
    JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64 \
    PATH=/android-sdk/cmdline-tools/latest/bin:/android-sdk/platform-tools:/android-sdk/tools/bin:$JAVA_HOME/bin:$PATH \
    DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    git \
    curl \
    zip \
    unzip \
    openjdk-17-jdk \
    nodejs \
    npm \
    build-essential \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Download Android SDK
RUN mkdir -p $ANDROID_HOME && \
    cd $ANDROID_HOME && \
    wget https://dl.google.com/android/repository/commandlinetools-linux-10406996_latest.zip && \
    unzip -q commandlinetools-linux-10406996_latest.zip && \
    rm commandlinetools-linux-10406996_latest.zip && \
    mkdir -p cmdline-tools/latest && \
    mv cmdline-tools/* cmdline-tools/latest/ 2>/dev/null || true

# Accept Android SDK licenses
RUN yes | sdkmanager --licenses

# Install required Android components
RUN sdkmanager \
    "platforms;android-35" \
    "build-tools;35.0.0" \
    "ndk;27.1.12297006" \
    "platform-tools" \
    "tools"

# Set working directory
WORKDIR /workspace

# Copy project files
COPY . /workspace/

# Install Node.js dependencies
RUN npm install

# Create debug keystore
RUN mkdir -p /root/.android && \
    keytool -genkey -v -keystore /root/.android/debug.keystore \
    -keyalg RSA -keysize 2048 -validity 10000 \
    -alias androiddebugkey -keypass android -storepass android \
    -dname "CN=Android Debug,O=Android,C=US"

# Build release APK
RUN cd android && \
    chmod +x gradlew && \
    ./gradlew assembleRelease --no-daemon

# Output APK to /outputs
RUN mkdir -p /outputs && \
    cp android/app/build/outputs/apk/release/app-release.apk /outputs/MarkerDetector-release.apk

CMD ["/bin/bash"]
