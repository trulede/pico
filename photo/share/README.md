# JPEG File Server

A lightweight Nginx Docker container that serves JPEG files over HTTPS from a mounted volume, optimized for Synology NAS (DS218).

## Features

- **Nginx-based** - Lightweight, fast, and efficient
- **HTTPS/SSL** - Secure JPEG file delivery with self-signed certificates
- **Zero Dependencies** - No Python or application runtime needed
- **Directory Listing** - Browse images via HTTP or JSON API
- **Security** - Blocks access to certificates and hidden files
- **NAS Optimized** - Minimal resource usage, ideal for DS218
- **Docker Only** - Simple `docker run` commands, no docker-compose needed

## Quick Start

### 1. Build the Image

```bash
make build
```

Or manually:
```bash
docker build -t jpeg-server .
```

### 2. Run the Container

```bash
make run
```

Or manually (adjust `IMAGES_DIR` to your photo directory):
```bash
docker run -d \
  --name jpeg-file-server \
  -p 80:80 \
  -p 443:443 \
  -v /mnt/photos:/app/images:ro \
  -v /tmp/jpeg-certs:/app/certs \
  --restart unless-stopped \
  jpeg-server
```

### 3. Verify Server

```bash
# Health check
curl http://localhost/health

# List images (HTTP redirects to HTTPS)
curl -k https://localhost/api/images

# For self-signed certificate warning, use -k flag
curl -k https://localhost/api/images
```

## Deployment on DS218

### Option 1: SSH/Command Line
```bash
ssh admin@192.168.1.100

docker run -d \
  --name jpeg-file-server \
  -p 80:80 \
  -p 443:443 \
  -v /volume1/photos:/app/images:ro \
  -v /volume1/docker/jpeg-certs:/app/certs \
  --restart unless-stopped \
  jpeg-server
```

### Option 2: Synology Docker UI
1. Open DSM → Package Center → Docker
2. Registry → Import Image
3. Upload the built image or search registry
4. Create container from the image
5. Set volume mounts and ports in settings

## API Endpoints

### Health Check
```
GET http://localhost/health
GET https://localhost/health
```
Returns: `healthy` (plain text)

### List All Images
```
GET https://localhost/api/images
```
Returns: JSON directory listing with all JPEG files

### Download Image
```
GET https://localhost/images/<filename>
```
Returns: JPEG file with proper MIME type

Example:
```bash
curl -k https://localhost/images/photo.jpg > photo.jpg
```

### Browse Images
```
GET https://localhost/images/
```
Returns: Directory listing (HTML or JSON based on Accept header)

## Usage on Pico

### Configuration in config.py

```python
# Secure connection to NAS image server
IMAGE_SERVER_URL = "https://192.168.1.100/images/"

# WiFi settings
WIFI_SSID = "your_network"
WIFI_PASSWORD = "your_password"
```

### Download Image from Pico

```python
from network import NetworkImageLoader
from main import JpegDisplay

loader = NetworkImageLoader()
loader.connect_wifi("your_ssid", "your_password")

# Download from HTTPS (self-signed certificate)
url = "https://192.168.1.100/images/photo.jpg"
loader.download_image(url, "images/photo.jpg")

display = JpegDisplay()
display.display_jpeg("images/photo.jpg", 0, 0)
```

### Disable SSL Verification (for self-signed certs)

```python
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

loader = NetworkImageLoader()
loader.connect_wifi("ssid", "password")
loader.download_image("https://192.168.1.100/images/photo.jpg", "images/photo.jpg")
```

## SSL/HTTPS Configuration

### Self-Signed Certificate

The Dockerfile automatically generates a self-signed certificate on first run. This is suitable for trusted networks like your home NAS.

**Certificate Details:**
- Valid for: 365 days
- Location in container: `/app/certs/cert.pem` and `/app/certs/key.pem`
- Generated automatically with Nginx Alpine's OpenSSL

### Using a Proper Certificate

To use a certificate from a Certificate Authority:

1. Obtain certificate and key files:
   - `cert.pem` - Your certificate
   - `key.pem` - Your private key

2. Mount to container with a host directory:
   ```bash
   docker run -d \
     --name jpeg-file-server \
     -p 80:80 \
     -p 443:443 \
     -v /mnt/photos:/app/images:ro \
     -v /path/to/certs:/app/certs:ro \
     jpeg-server
   ```

3. Nginx will use your certificates automatically

## Performance

### Resource Usage
- **Image size:** ~20 MB (Nginx Alpine)
- **Memory:** ~10-20 MB idle
- **CPU:** Minimal (event-driven)

### Optimization for DS218
- Read-only volume mount for images (safer)
- Gzip compression enabled
- HTTP/2 support
- Connection pooling

## Troubleshooting

### Port Already in Use

```bash
# Check what's using the ports
lsof -i :80
lsof -i :443

# Use different ports
docker run -d \
  --name jpeg-file-server \
  -p 8080:80 \
  -p 8443:443 \
  -v /mnt/photos:/app/images:ro \
  jpeg-server
```

### Cannot Access Images

```bash
# Check container is running
docker ps | grep jpeg-file-server

# Check logs
docker logs jpeg-file-server

# Verify volume permissions
docker exec jpeg-file-server ls -la /app/images
```

### Certificate Errors

```bash
# The certificate is self-signed, so curl needs -k flag
curl -k https://localhost/api/images

# Or disable warnings in Pico:
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
```

### No Images Showing

1. Verify volume mount path exists:
   ```bash
   docker inspect jpeg-file-server | grep -A 5 "Mounts"
   ```

2. Check folder has JPEG files:
   ```bash
   docker exec jpeg-file-server ls /app/images
   ```

3. Check file permissions:
   ```bash
   docker exec jpeg-file-server stat /app/images/photo.jpg
   ```

## Make Targets

```bash
make help      # Show all available targets
make build     # Build Docker image
make run       # Start container
make stop      # Stop container
make logs      # View container logs
make remove    # Remove container
make clean     # Remove container and image
```

## Security Notes

- **Read-only images:** Volume mounted as `:ro` prevents accidental modifications
- **Blocked paths:** `/certs/` and hidden files (`.` prefix) are blocked
- **HTTPS:** All traffic is encrypted with SSL/TLS
- **Headers:** Security headers included (HSTS, X-Content-Type-Options, etc.)
- **Self-signed:** Certificate warning is normal for self-signed certs

## References

- [Nginx Official Docker Image](https://hub.docker.com/_/nginx)
- [Synology Docker Guide](https://www.synology.com/)
- [Nginx SSL Configuration](https://nginx.org/en/docs/http/ngx_http_ssl_module.html)
