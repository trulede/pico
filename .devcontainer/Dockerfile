# Dockerfile for MicroPython and Pico SDK Development
# Base image: Python 3.11 with build essentials
FROM mcr.microsoft.com/devcontainers/python:1-3.11-bullseye

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    curl \
    gcc-arm-none-eabi \
    git \
    libnewlib-arm-none-eabi \
    libstdc++-arm-none-eabi-newlib \
    libusb-1.0-0-dev \
    minicom \
    openocd \
    picocom \
    rsync \
    screen \
    tar \
    unzip \
    wget \
    apt-transport-https \
    ca-certificates \
    gnupg \
    lsb-release \
    && rm -rf /var/lib/apt/lists/*

# Install Docker CLI version 1.4.3
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends docker-ce-cli=5:20.10.24~3-0~debian-bullseye && \
    rm -rf /var/lib/apt/lists/*

# Install Docker Buildx
RUN mkdir -p ~/.docker/cli-plugins/ && \
    curl -SL https://github.com/docker/buildx/releases/latest/download/buildx-$(uname -m) -o ~/.docker/cli-plugins/docker-buildx && \
    chmod +x ~/.docker/cli-plugins/docker-buildx
    
# Install MicroPython tools
RUN pip install --no-cache-dir \
    black \
    pylint \
    pytest

# Set up Pico SDK
ENV PICO_SDK_PATH=/opt/pico-sdk/pico-sdk
RUN git clone --depth=1 https://github.com/raspberrypi/pico-sdk.git "$PICO_SDK_PATH"

# Set up Pico Tool
ENV PICO_TOOL_PATH=/opt/picotool/picotool
RUN git clone --depth=1 https://github.com/raspberrypi/picotool.git "$PICO_TOOL_PATH"
RUN cd $PICO_TOOL_PATH; mkdir build; cd build; export PICO_SDK_PATH=$PICO_SDK_PATH; cmake ../; make

# Setup Micropython
ENV MICROPYTHON_PATH=/opt/micropython/micropython
RUN git clone --depth=1 https://github.com/micropython/micropython.git "$MICROPYTHON_PATH"
RUN cd $MICROPYTHON_PATH; make -C ports/rp2 submodules; make -C mpy-cross

# Set up user (for VS Code devcontainer best practices)
ARG USERNAME=vscode
USER root
RUN groupadd -f docker && usermod -aG dialout,plugdev,docker $USERNAME
USER $USERNAME


# Enable BuildKit by default
ENV DOCKER_BUILDKIT=1

# Set working directory
WORKDIR /workspaces/pico

# Default shell
SHELL ["/bin/bash", "-c"]

# Display version info for verification
RUN python --version && gcc --version && cmake --version && arm-none-eabi-gcc --version

# Entrypoint
CMD ["/bin/bash"]
