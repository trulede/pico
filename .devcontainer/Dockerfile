# Dockerfile for MicroPython Pico Devcontainer
FROM mcr.microsoft.com/devcontainers/python:1-3.11-bullseye

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        minicom \
        screen \
        picocom \
        rshell \
        python3-pip \
        git \
        build-essential \
        gcc-arm-none-eabi \
        libnewlib-arm-none-eabi \
        libstdc++-arm-none-eabi-newlib \
        openocd \
        wget \
        unzip \
        make \
        cmake && \
    rm -rf /var/lib/apt/lists/*

# Install Python tools for MicroPython
RUN pip install --upgrade pip && \
    pip install esptool adafruit-ampy micropython-stubs black pylint pytest

# Install Pico SDK
RUN mkdir -p /opt/pico-sdk && \
    git clone --depth=1 https://github.com/raspberrypi/pico-sdk.git /opt/pico-sdk/pico-sdk && \
    chown -R vscode:vscode /opt/pico-sdk

ENV PICO_SDK_PATH=/opt/pico-sdk/pico-sdk
