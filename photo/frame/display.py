"""
Display utilities for Picographics with JPEGDEC support
"""
from machine import Pin, SPI
import picographics


class DisplayManager:
    """Manages Picographics display initialization and operations"""
    
    def __init__(self, display_type=picographics.DISPLAY_PICO_EXPLORER):
        """
        Initialize the display
        
        Args:
            display_type: Type of Picographics display
        """
        self.display_type = display_type
        self.spi = None
        self.display = None
        self._init_display()
    
    def _init_display(self):
        """Initialize SPI and Picographics display"""
        self.spi = SPI(0, baudrate=12000000, polarity=1, phase=1, bits=8,
                       firstbit=SPI.MSB, sck=Pin(18), mosi=Pin(19), 
                       miso=Pin(16))
        
        self.display = picographics.PicoGraphics(
            display=self.display_type,
            spi=self.spi,
            cs=Pin(17),
            dc=Pin(20),
            rst=Pin(21)
        )
    
    def clear(self):
        """Clear the display"""
        self.display.clear()
        self.display.update()
    
    def update(self):
        """Update the display"""
        self.display.update()
    
    def get_display(self):
        """Get the raw display object for direct manipulation"""
        return self.display
    
    def get_width(self):
        """Get display width in pixels"""
        return self.display.get_width()
    
    def get_height(self):
        """Get display height in pixels"""
        return self.display.get_height()
    
    def set_pen(self, color):
        """Set the pen color"""
        self.display.set_pen(color)
    
    def pixel(self, x, y):
        """Draw a pixel at (x, y)"""
        self.display.pixel(x, y)
    
    def text(self, string, x, y, max_width=None, character_spacing=1):
        """Draw text on display"""
        self.display.text(string, x, y, max_width, character_spacing)
