"""
JPEG utilities using BitBank's JPEGDEC library
"""
import jpegdec


class JpegDecoder:
    """Wrapper for JPEGDEC library functionality"""
    
    def __init__(self):
        """Initialize JPEGDEC decoder"""
        self.decoder = jpegdec.JPEGDEC()
        self.width = 0
        self.height = 0
    
    def open_file(self, filename):
        """
        Open a JPEG file for decoding
        
        Args:
            filename: Path to JPEG file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            result = self.decoder.openFile(filename, self._draw_callback)
            return result == jpegdec.JPEG_SUCCESS
        except Exception as e:
            print(f"Error opening JPEG file {filename}: {e}")
            return False
    
    def decode(self, x=0, y=0, scale=jpegdec.JPEG_SCALE_FULL):
        """
        Decode and display JPEG
        
        Args:
            x: X coordinate for display
            y: Y coordinate for display
            scale: Scale factor (JPEG_SCALE_FULL, JPEG_SCALE_HALF, etc.)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            result = self.decoder.decode(x, y, scale)
            return result == jpegdec.JPEG_SUCCESS
        except Exception as e:
            print(f"Error decoding JPEG: {e}")
            return False
    
    def get_width(self):
        """Get decoded image width"""
        return self.decoder.getWidth()
    
    def get_height(self):
        """Get decoded image height"""
        return self.decoder.getHeight()
    
    def close(self):
        """Close the JPEG decoder"""
        try:
            self.decoder.close()
        except Exception as e:
            print(f"Error closing JPEG decoder: {e}")
    
    def _draw_callback(self, x, y, w, h, data):
        """
        Callback function called during JPEG decoding
        Override this in subclass for custom drawing
        
        Args:
            x, y: Position
            w, h: Width and height
            data: Pixel data
        """
        pass
