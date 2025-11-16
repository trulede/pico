# Pico MicroPython Development

A collection of MicroPython applications for Raspberry Pi Pico with a pre-configured development container.

## Applications

### photo/frame - JPEG Display Application
A MicroPython application that displays JPEG images on a Pimori Picographics display using BitBank's JPEGDEC library for efficient decoding.

**Features:**
- Displays JPEG images on Picographics displays
- Uses optimized JPEGDEC decoder
- Includes display and JPEG utilities
- Network image loading support
- Simple build and deployment workflow
- WiFi configuration management

**Location:** `/photo/frame`

**Quick Start:**
```bash
cd photo/frame
make config     # Configure WiFi credentials
make download   # Download MicroPython firmware
make flash      # Flash to Pico (hold BOOTSEL)
make install    # Install required modules
make upload     # Upload application to Pico
```

### photo/share - JPEG File Server
A lightweight Nginx Docker container that serves JPEG images over HTTPS from a mounted volume on your NAS, enabling the Pico to fetch images over the network.

**Features:**
- HTTPS/SSL secure file serving
- Minimal resource usage (Nginx Alpine ~20 MB)
- Auto-generated self-signed certificates
- Directory listing API
- Optimized for Synology NAS (DS218)
- Read-only volume mounts for safety
- No external dependencies (pure Nginx)

**Location:** `/photo/share`

**Quick Start (on NAS):**
```bash
cd photo/share
# Edit Makefile: set IMAGES_DIR to your NAS photo directory
make build      # Build Docker image: pico-photo-share
make run        # Start container
curl -k https://localhost/api/images  # Verify
```

**Integration with photo/frame:**
The photo/frame application can fetch images from photo/share via the network:
```python
# In photo/frame/config.py
WIFI_SSID = "your_network"
WIFI_PASSWORD = "your_password"
IMAGE_SERVER_URL = "https://192.168.1.100/images/"
```

Then the Pico automatically downloads and displays images from your NAS!

## Development Setup

### Using VS Code Dev Container

1. **Install Prerequisites:**
   - VS Code
   - Docker or Docker Desktop
   - VS Code Remote - Containers extension

2. **Open in Dev Container:**
   - Open this folder in VS Code
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
   - Type "Dev Containers: Open Folder in Container"
   - Wait for the container to build and start

3. **You're Ready!**
   - All tools are pre-installed
   - Pico SDK is configured
   - Start developing with `make` commands

### Available Tools in Dev Container

- **Python 3.11** with development tools
- **MicroPython Tools:**
  - rshell - Remote shell for device communication
  - esptool - Flashing tool
  - adafruit-ampy - File operations
  - micropython-stubs - Type hints
- **Embedded Development:**
  - ARM Toolchain (gcc-arm-none-eabi)
  - Pico SDK at `/opt/pico-sdk/pico-sdk`
  - OpenOCD for debugging
- **Serial Communication:**
  - minicom, screen, picocom
- **Code Quality:**
  - Black formatter
  - Pylint
  - Pytest

### VS Code Extensions (Auto-installed)

- Python
- Pylance
- Debugpy
- Ruff
- Makefile Tools
- Raspberry Pi Pico SDK
- Pico-W-Go
- C/C++ Tools

## Project Structure

```
.devcontainer/          # Dev container configuration
  ├── Dockerfile        # Container build configuration
  └── devcontainer.json # VS Code container settings
photo/
  ├── frame/            # JPEG Display application (Pico)
  │   ├── main.py       # Main application
  │   ├── display.py    # Display utilities
  │   ├── jpeg.py       # JPEG decoder wrapper
  │   ├── network.py    # Network/WiFi utilities
  │   ├── network_example.py # Network usage examples
  │   ├── config.example.py  # WiFi configuration template
  │   ├── Makefile      # Build automation
  │   ├── requirements.txt   # Python dependencies
  │   ├── README.md     # App documentation
  │   └── images/       # JPEG image files
  └── share/            # JPEG File Server (Docker/Nginx)
      ├── Dockerfile    # Nginx container configuration
      ├── nginx.conf    # Nginx main config
      ├── nginx-ssl.conf # SSL/HTTPS configuration
      ├── Makefile      # Docker management
      ├── requirements.txt # Reference (no dependencies)
      ├── .gitignore    # Exclude certificates
      └── README.md     # Server documentation
```

## Hardware

- **Raspberry Pi Pico** microcontroller with display
- **Pimori Picographics Display** (or compatible) - for photo/frame
- **Synology NAS (DS218)** or compatible - for photo/share Docker container
- **USB Cable** for Pico programming and communication
- **WiFi** - for Pico to connect to NAS image server (optional, required for network images)

## System Architecture

```
Your Photos on NAS
        ↓
[photo/share - Docker/Nginx]
   HTTPS Server on DS218
        ↓ (WiFi)
[Pico with Display]
[photo/frame - MicroPython]
   Shows images from server
```

## Workflow

1. **Setup Development Environment:**
   - Open workspace in VS Code Dev Container
   - All MicroPython tools pre-installed

2. **Deploy Image Server:**
   - Build and run photo/share Docker container on NAS
   - Serves your photo library via HTTPS

3. **Configure Pico Application:**
   - Run `make config` in photo/frame
   - Set WiFi credentials and NAS server URL

4. **Flash and Deploy:**
   - `make download` - Get firmware
   - `make flash` - Flash to Pico (BOOTSEL mode)
   - `make upload` - Deploy app to Pico

5. **Enjoy:**
   - Pico connects to WiFi
   - Fetches images from NAS
   - Displays on Picographics display

## Resources

- [Raspberry Pi Pico Documentation](https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html)
- [MicroPython Documentation](https://docs.micropython.org/)
- [Pimori Pimoroni Pico Libraries](https://github.com/pimoroni/pimoroni-pico)
- [BitBank JPEGDEC](https://github.com/bitbank2/JPEGDEC)