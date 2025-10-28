#!/bin/bash

set -e

echo "🧹 Cleaning Docker Images and Containers"
echo "=========================================="

# Detect docker compose command
if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
elif docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
else
    echo "❌ docker compose is not available. Please install Docker Compose and try again."
    exit 1
fi

# Function to ask for confirmation
confirm() {
    read -p "❓ $1 (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        return 0
    else
        return 1
    fi
}

# Stop and remove containers
if confirm "Stop and remove all containers?"; then
    echo "🛑 Stopping containers..."
    $COMPOSE_CMD down || true
    echo "✅ Containers stopped and removed"
fi

# Remove images
if confirm "Remove Volcengine Docker images?"; then
    echo "🗑️  Removing images..."
    docker images | grep volcengine | awk '{print $3}' | xargs -r docker rmi -f || true
    echo "✅ Images removed"
fi

# Remove volumes
if confirm "Remove Docker volumes (WARNING: this will delete data)?"; then
    echo "🗑️  Removing volumes..."
    $COMPOSE_CMD down -v || true
    echo "✅ Volumes removed"
fi

# Prune system
if confirm "Run Docker system prune (remove unused data)?"; then
    echo "🧹 Pruning Docker system..."
    docker system prune -f
    echo "✅ System pruned"
fi

echo ""
echo "🎉 Cleanup completed!"
echo ""
echo "📊 Current Docker status:"
echo "Images:"
docker images | head -n 5
echo ""
echo "Containers:"
docker ps -a | head -n 5
