"""
Network folder utilities for loading images from HTTP URLs
MicroPython compatible network image loading
"""
import network
import time


class NetworkImageLoader:
    """Load images from network shares and HTTP URLs"""
    
    def __init__(self):
        """Initialize network utilities"""
        self.wlan = None
        self.connected = False
    
    def connect_wifi(self, ssid, password):
        """
        Connect to WiFi network
        
        Args:
            ssid: WiFi network name
            password: WiFi password
            
        Returns:
            True if connected, False otherwise
        """
        try:
            self.wlan = network.WLAN(network.STA_IF)
            self.wlan.active(True)
            self.wlan.connect(ssid, password)
            
            # Wait for connection
            max_wait = 10
            while max_wait > 0:
                if self.wlan.status() < 0 or self.wlan.status() >= 3:
                    break
                max_wait -= 1
                print(f"Waiting for connection... ({max_wait}s)")
                time.sleep(1)
            
            if self.wlan.status() == 3:
                self.connected = True
                print(f"✓ Connected! IP: {self.wlan.ifconfig()[0]}")
                return True
            else:
                print("✗ Connection failed")
                return False
        except Exception as e:
            print(f"Error connecting to WiFi: {e}")
            return False
    
    def download_image(self, url, destination_path):
        """
        Download image from HTTP/HTTPS URL
        
        Args:
            url: URL to image file
            destination_path: Local path to save image
            
        Returns:
            True if successful, False otherwise
        """
        if not self.connected:
            print("✗ Not connected to network")
            return False
        
        try:
            import urllib.request
            
            print(f"Downloading from {url}...")
            response = urllib.request.urlopen(url)
            
            with open(destination_path, 'wb') as f:
                f.write(response.read())
            
            print(f"✓ Downloaded to {destination_path}")
            return True
        except Exception as e:
            print(f"Error downloading image: {e}")
            return False
    
    def load_from_smb(self, smb_path, username, password, destination_path):
        """
        Load image from SMB/network share (Not supported on standard MicroPython)
        
        For SMB access, consider using HTTP-based file sharing or FTP instead.
        
        Args:
            smb_path: Path like \\server\share\image.jpg
            username: SMB username
            password: SMB password
            destination_path: Local path to save image
            
        Returns:
            True if successful, False otherwise
        """
        print("✗ SMB is not supported on standard MicroPython")
        print("  Alternatives:")
        print("  1. Use HTTP/HTTPS URLs with download_image()")
        print("  2. Set up an FTP server and use FTP client")
        print("  3. Use WebDAV or other HTTP-based protocols")
        return False
    
    def disconnect_wifi(self):
        """Disconnect from WiFi"""
        if self.wlan:
            self.wlan.disconnect()
            self.connected = False
            print("✓ Disconnected from WiFi")
    
    def get_signal_strength(self):
        """Get WiFi signal strength in dBm"""
        if self.wlan and self.connected:
            return self.wlan.status('rssi')
        return None
