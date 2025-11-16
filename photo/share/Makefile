.PHONY: help build run stop logs clean remove certs

IMAGE_NAME := pico-photo-share
CONTAINER_NAME := pico-photo-share
IMAGES_DIR := /mnt/photos
PORT_HTTP := 80
PORT_HTTPS := 443

help:
	@echo "JPEG File Server - Nginx Docker"
	@echo "================================"
	@echo ""
	@echo "Targets:"
	@echo "  make build      - Build Docker image"
	@echo "  make run        - Start container"
	@echo "  make stop       - Stop running container"
	@echo "  make logs       - Show container logs"
	@echo "  make remove     - Remove container"
	@echo "  make clean      - Remove container and image"
	@echo ""
	@echo "Quick Start:"
	@echo "  1. Edit Makefile: set IMAGES_DIR to your photo directory"
	@echo "  2. make build"
	@echo "  3. make run"
	@echo "  4. curl https://localhost/api/images (may need --insecure for self-signed cert)"

build:
	@echo "Building Docker image: $(IMAGE_NAME)..."
	@docker build -t $(IMAGE_NAME) .
	@echo "✓ Image built successfully"

run: build
	@echo "Starting container: $(CONTAINER_NAME)..."
	@docker run -d \
		--name $(CONTAINER_NAME) \
		-p $(PORT_HTTP):80 \
		-p $(PORT_HTTPS):443 \
		-v $(IMAGES_DIR):/app/images:ro \
		-v /tmp/jpeg-certs:/app/certs \
		--restart unless-stopped \
		$(IMAGE_NAME)
	@echo "✓ Container started"
	@echo "  HTTP:  http://localhost:$(PORT_HTTP)/api/images"
	@echo "  HTTPS: https://localhost:$(PORT_HTTPS)/api/images (self-signed)"
	@echo ""
	@echo "Note: For HTTPS, use: curl -k https://localhost/api/images"

stop:
	@echo "Stopping container..."
	@docker stop $(CONTAINER_NAME) 2>/dev/null || true
	@echo "✓ Container stopped"

logs:
	@echo "Showing container logs..."
	@docker logs -f $(CONTAINER_NAME)

remove: stop
	@echo "Removing container..."
	@docker rm $(CONTAINER_NAME) 2>/dev/null || true
	@echo "✓ Container removed"

clean: remove
	@echo "Removing Docker image..."
	@docker rmi $(IMAGE_NAME) 2>/dev/null || true
	@echo "✓ Image removed"

.DEFAULT_GOAL := help
