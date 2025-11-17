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
    && rm -rf /var/lib/apt/lists/*

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
RUN usermod -aG dialout,plugdev $USERNAME
USER $USERNAME

# Set working directory
WORKDIR /workspaces/pico

# Default shell
SHELL ["/bin/bash", "-c"]

# Display version info for verification
RUN python --version && gcc --version && cmake --version && arm-none-eabi-gcc --version

# Entrypoint
CMD ["/bin/bash"]
