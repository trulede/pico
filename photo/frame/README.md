# Pimori Picographics JPEG Display Application

MicroPython application for displaying JPEG images on a Pico using Pimori Picographics and BitBank's JPEGDEC library.

## Files

- `main.py` - Main application with JpegDisplay class for integrated display and JPEG handling
- `display.py` - DisplayManager utility for Picographics display operations
- `jpeg.py` - JpegDecoder wrapper for JPEGDEC library functionality
- `images/` - Directory for JPEG image files

## Hardware Requirements

- Raspberry Pi Pico
- Pimori Picographics display (or compatible display)
- SPI connection (default pins: SCK=18, MOSI=19, MISO=16, CS=17, DC=20, RST=21)

## Dependencies

- Pimori Picographics library
- BitBank JPEGDEC library (for efficient JPEG decoding)

Both should be included with MicroPython Pico firmware from Pimori.

## Installation

1. Flash MicroPython firmware to Pico that includes Picographics and JPEGDEC
2. Place JPEG images in the `images/` directory
3. Deploy application files to Pico:
   ```bash
   rshell
   > cp -r app/* /pyboard/
   ```

## Usage

### Basic Image Display

```python
from main import JpegDisplay

# Initialize display
display = JpegDisplay()

# Display JPEG image
display.display_jpeg("images/image.jpg", 0, 0)
```

### Using DisplayManager

```python
from display import DisplayManager

# Initialize display
dm = DisplayManager()

# Get display info
width = dm.get_width()
height = dm.get_height()

# Draw text
dm.set_pen(0xFFFFFF)  # White
dm.text("Hello Pico!", 10, 10)
dm.update()
```

### Using JpegDecoder Directly

```python
from jpeg import JpegDecoder
import jpegdec

# Initialize decoder
decoder = JpegDecoder()

# Open and decode JPEG
if decoder.open_file("images/image.jpg"):
    decoder.decode(0, 0, jpegdec.JPEG_SCALE_FULL)
    print(f"Image: {decoder.get_width()}x{decoder.get_height()}")
```

## Pin Configuration

Default SPI pins:
- SCK: GPIO 18
- MOSI: GPIO 19
- MISO: GPIO 16
- CS: GPIO 17
- DC: GPIO 20
- RST: GPIO 21

Modify pin numbers in `display.py` if using different pins.

## Display Types

Modify `display_type` parameter in `main.py` for different displays:
- `picographics.DISPLAY_PICO_EXPLORER`
- `picographics.DISPLAY_1_54_RGB`
- `picographics.DISPLAY_PICO_DISPLAY`

See Pimori documentation for full list of supported displays.

## Performance Tips

- Use appropriate JPEG scale factors to reduce decoding time
- JPEGDEC is optimized for JPEG decoding on microcontrollers
- Picographics handles efficient display updates

## References

- [Pimori Documentation](https://github.com/pimoroni/pimoroni-pico)
- [BitBank JPEGDEC](https://github.com/bitbank2/JPEGDEC)
- [Raspberry Pi Pico](https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html)
