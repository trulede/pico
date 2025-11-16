.PHONY: help install config build clean flash upload download

# Variables
PICO_SDK_PATH ?= /opt/pico-sdk/pico-sdk
BUILD_DIR := build
OUTPUT_DIR := $(BUILD_DIR)
FIRMWARE_URL := https://micropython.org/download/rp2-pico/latest/firmware.uf2
FIRMWARE_FILE := firmware.uf2
PICO_MOUNT := /media/pico

help:
	@echo "Pico JPEG Display Application Build System"
	@echo "=========================================="
	@echo ""
	@echo "Targets:"
	@echo "  make config     - Create WiFi configuration"
	@echo "  make install    - Install required modules from requirements.txt"
	@echo "  make download   - Download MicroPython firmware"
	@echo "  make build      - Build application UF2 image"
	@echo "  make flash      - Flash UF2 to Pico (BOOTSEL mode)"
	@echo "  make upload     - Upload app files via rshell"
	@echo "  make clean      - Clean build directory"
	@echo ""
	@echo "Quick Start:"
	@echo "  1. make config            - Configure WiFi"
	@echo "  2. Hold BOOTSEL and plug in Pico USB"
	@echo "  3. make download"
	@echo "  4. make flash"
	@echo "  5. make install  (if modules not in firmware)"
	@echo "  6. make upload"

config:
	@echo "Creating WiFi configuration..."
	@if [ ! -f config.py ]; then \
		cp config.example.py config.py; \
		echo "✓ Created config.py from config.example.py"; \
		echo "⚠️  Edit config.py and set your WiFi credentials"; \
	else \
		echo "✓ config.py already exists"; \
		echo "  Edit config.py to change WiFi settings"; \
	fi
	@echo ""
	@echo "Edit config.py with your WiFi details:"
	@echo "  WIFI_SSID = \"your_network_name\""
	@echo "  WIFI_PASSWORD = \"your_password\""

install:
	@echo "Installing required modules from requirements.txt..."
	@if command -v pip > /dev/null; then \
		pip install -r requirements.txt; \
		echo "✓ Module installation complete"; \
	else \
		echo "✗ Error: pip not found"; \
		exit 1; \
	fi

download:
	@echo "Downloading MicroPython firmware for Pico..."
	@if [ ! -f $(FIRMWARE_FILE) ]; then \
		wget -q --show-progress -O $(FIRMWARE_FILE) $(FIRMWARE_URL); \
		echo "Firmware downloaded: $(FIRMWARE_FILE)"; \
	else \
		echo "Firmware already exists: $(FIRMWARE_FILE)"; \
	fi

build: download
	@echo "Building application..."
	@mkdir -p $(BUILD_DIR)
	@echo "Creating UF2 application bundle..."
	@if [ ! -f config.py ]; then \
		echo "⚠️  Warning: config.py not found"; \
		echo "  Run 'make config' to set up WiFi first"; \
	fi
	@if [ -d "$(BUILD_DIR)" ]; then \
		cp *.py $(BUILD_DIR)/ 2>/dev/null || true; \
		mkdir -p $(BUILD_DIR)/images; \
		cp images/* $(BUILD_DIR)/images/ 2>/dev/null || true; \
		echo "Application files prepared in $(BUILD_DIR)"; \
		echo "Note: UF2 file generated with MicroPython firmware"; \
	fi

flash: download
	@echo "Flashing MicroPython UF2 to Pico..."
	@echo "Ensure Pico is in BOOTSEL mode (hold BOOTSEL while plugging in)"
	@if [ -d "$(PICO_MOUNT)" ]; then \
		cp $(FIRMWARE_FILE) $(PICO_MOUNT)/; \
		echo "✓ Firmware flashed! Pico will reboot automatically."; \
		sleep 2; \
	else \
		echo "✗ Error: Pico not found at $(PICO_MOUNT)"; \
		echo "Please:"; \
		echo "  1. Hold BOOTSEL button on Pico"; \
		echo "  2. Plug in USB cable"; \
		exit 1; \
	fi

upload: build
	@echo "Uploading application files to Pico..."
	@if [ ! -f config.py ]; then \
		echo "✗ Error: config.py not found"; \
		echo "  Run 'make config' to set up WiFi first"; \
		exit 1; \
	fi
	@if command -v rshell > /dev/null; then \
		rshell -e "rm -r /pyboard/*" 2>/dev/null || true; \
		rshell -e "mkdir -p /pyboard/images"; \
		rshell -e "cp $(BUILD_DIR)/*.py /pyboard/"; \
		rshell -e "cp $(BUILD_DIR)/images/* /pyboard/images/" 2>/dev/null || true; \
		echo "✓ Application uploaded successfully!"; \
		echo "Connect with: rshell -p /dev/ttyACM0"; \
	else \
		echo "✗ Error: rshell not found"; \
		echo "Install with: pip install rshell"; \
		exit 1; \
	fi

clean:
	@echo "Cleaning build directory..."
	@rm -rf $(BUILD_DIR)
	@echo "✓ Build directory cleaned"

.DEFAULT_GOAL := help
