"""
Example: Load and display image from network folder
Uses WiFi configuration from config.py
"""
from network import NetworkImageLoader
from main import JpegDisplay
import time

# Import configuration
try:
    from config import WIFI_SSID, WIFI_PASSWORD, IMAGE_SERVER_URL
except ImportError:
    print("✗ config.py not found!")
    print("  Run 'make config' to create it")
    WIFI_SSID = None
    WIFI_PASSWORD = None
    IMAGE_SERVER_URL = None


def example_http_image():
    """Example: Load image from HTTP URL using config"""
    print("=== HTTP Image Loading Example ===\n")
    
    if not WIFI_SSID or not WIFI_PASSWORD:
        print("✗ WiFi credentials not configured")
        print("  Run 'make config' and edit config.py")
        return
    
    # Initialize network loader
    loader = NetworkImageLoader()
    
    # Connect to WiFi using config
    if not loader.connect_wifi(WIFI_SSID, WIFI_PASSWORD):
        print("Failed to connect to WiFi")
        return
    
    # Download image from HTTP URL
    url = IMAGE_SERVER_URL + "image.jpg" if IMAGE_SERVER_URL else "http://example.com/image.jpg"
    local_path = "images/network_image.jpg"
    
    if loader.download_image(url, local_path):
        # Display the downloaded image
        display = JpegDisplay()
        display.display_jpeg(local_path, 0, 0)
        print("Image displayed!")
    else:
        print("Failed to download image")
    
    # Disconnect
    loader.disconnect_wifi()


def example_periodic_update():
    """Example: Periodically load and display images from network"""
    print("=== Periodic Network Image Update Example ===\n")
    
    if not WIFI_SSID or not WIFI_PASSWORD:
        print("✗ WiFi credentials not configured")
        print("  Run 'make config' and edit config.py")
        return
    
    loader = NetworkImageLoader()
    display = JpegDisplay()
    
    # Connect to WiFi using config
    if not loader.connect_wifi(WIFI_SSID, WIFI_PASSWORD):
        print("Failed to connect to WiFi")
        return
    
    update_interval = 3600  # Update every hour (in seconds)
    
    try:
        while True:
            print("Fetching image from network...")
            url = IMAGE_SERVER_URL + "current.jpg" if IMAGE_SERVER_URL else "http://example.com/current_image.jpg"
            local_path = "images/current.jpg"
            
            if loader.download_image(url, local_path):
                display.display_jpeg(local_path, 0, 0)
                print(f"✓ Image updated")
            else:
                print("✗ Failed to fetch image")
            
            # Wait for next update
            print(f"Next update in {update_interval}s\n")
            time.sleep(update_interval)
    except KeyboardInterrupt:
        print("Stopping periodic updates")
        loader.disconnect_wifi()


if __name__ == "__main__":
    # Uncomment one example to run:
    # example_http_image()
    # example_periodic_update()
    
    print("Network image loading examples")
    print("See comments to run examples")

