# Define phony targets to avoid conflicts with file names
.PHONY: info build up down clean logs shell

# Show available commands
info:
	@echo "📦 Available Makefile Commands:"
	@echo ""
	@echo "  make info    → Show this help message"
	@echo "  make build   → Build the Docker image"
	@echo "  make up      → Start the application (detached)"
	@echo "  make down    → Stop and remove containers"
	@echo "  make logs    → Follow live container logs"
	@echo "  make clean   → Prune unused Docker objects"
	@echo ""

# Build the Docker image
build:
	docker-compose build

# Run the application in detached mode (background)
up:
	docker-compose up -d
	@echo "Gym App is running at http://localhost:8501"

# Stop the application and remove containers
down:
	docker-compose down

# View live logs from the container
logs:
	docker-compose logs -f

# Clean up docker system - Use with caution
clean:
	docker system prune -f
