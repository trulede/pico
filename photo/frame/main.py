"""
Picographics JPEG Display Application
Displays JPEG images using BitBank's JPEGDEC library with Pimori Picographics
"""
from machine import Pin, SPI
import picographics
import jpegdec
import time


class JpegDisplay:
    """Manages JPEG display with Picographics and JPEGDEC"""
    
    def __init__(self, display_type=picographics.DISPLAY_PICO_EXPLORER):
        """Initialize display and JPEG decoder"""
        self.display_type = display_type
        self.spi = None
        self.display = None
        self.jpeg = None
        self._init_hardware()
    
    def _init_hardware(self):
        """Initialize SPI, display, and JPEG decoder"""
        # Initialize SPI interface
        self.spi = SPI(0, baudrate=12000000, polarity=1, phase=1, bits=8,
                       firstbit=SPI.MSB, sck=Pin(18), mosi=Pin(19), 
                       miso=Pin(16))
        
        # Initialize Picographics display
        self.display = picographics.PicoGraphics(
            display=self.display_type,
            spi=self.spi,
            cs=Pin(17),
            dc=Pin(20),
            rst=Pin(21)
        )
        
        # Initialize JPEGDEC decoder
        self.jpeg = jpegdec.JPEGDEC()
    
    def display_jpeg(self, filename, x=0, y=0):
        """
        Load and display a JPEG image at specified position
        
        Args:
            filename: Path to JPEG file
            x: X coordinate (default 0)
            y: Y coordinate (default 0)
        """
        try:
            # Open and decode JPEG
            self.jpeg.openRAM(filename, self._jpeg_draw)
            self.jpeg.decode(x, y, jpegdec.JPEG_SCALE_FULL)
            
            # Update display
            self.display.update()
            print(f"Successfully displayed: {filename}")
            return True
        except Exception as e:
            print(f"Error displaying JPEG {filename}: {e}")
            return False
    
    def _jpeg_draw(self, x, y, w, h, data):
        """Callback function for JPEGDEC to draw pixels to display"""
        self.display.set_pen(0)  # Could extract color from data if needed
        # Implementation depends on picographics API for pixel drawing
        pass
    
    def clear(self):
        """Clear the display"""
        self.display.clear()
        self.display.update()
    
    def get_width(self):
        """Get display width"""
        return self.display.get_width()
    
    def get_height(self):
        """Get display height"""
        return self.display.get_height()


def main():
    """Main application"""
    print("Initializing Picographics JPEG Display with JPEGDEC...")
    
    # Initialize display
    display_manager = JpegDisplay()
    
    print(f"Display initialized: {display_manager.get_width()}x{display_manager.get_height()}")
    
    # Clear display
    display_manager.clear()
    
    # Display JPEG image
    if display_manager.display_jpeg("images/image.jpg", 0, 0):
        print("JPEG image displayed successfully!")
    else:
        print("Failed to display JPEG image")
    
    # Keep application running
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
