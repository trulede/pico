# JPEG File Server - Nginx
# Serves JPEG files over HTTP/HTTPS from a mounted volume

FROM nginx:alpine

# Install openssl for certificate generation
RUN apk add --no-cache openssl

# Create directories
RUN mkdir -p /app/images /app/certs /etc/nginx/conf.d

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf
COPY nginx-ssl.conf /etc/nginx/conf.d/default.conf

# Create self-signed certificate if not present
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /app/certs/key.pem \
    -out /app/certs/cert.pem \
    -subj "/C=US/ST=State/L=City/O=Organization/CN=jpeg-server" \
    || true

# Volume for JPEG files and certificates
VOLUME ["/app/images", "/app/certs"]

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost/health || exit 1

# Expose ports
EXPOSE 80 443

# Run nginx
CMD ["nginx", "-g", "daemon off;"]
