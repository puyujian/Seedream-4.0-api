#!/bin/bash

set -e

echo "🚀 Starting Volcengine Image Generator"
echo "======================================"

# Detect docker compose command
if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
elif docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
else
    echo "❌ docker compose is not available. Please install Docker Compose and try again."
    exit 1
fi

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found, creating from example..."
    cp .env.example .env
    echo "✅ Created .env file. Please edit it with your credentials if needed."
    echo "   (Application will run in demo mode without credentials)"
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

echo ""
echo "📦 Building Docker images..."
$COMPOSE_CMD build

echo ""
echo "🎬 Starting services..."
$COMPOSE_CMD up -d

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 5

# Check if services are running
if $COMPOSE_CMD ps | grep -q "Up"; then
    echo ""
    echo "✅ Application started successfully!"
    echo ""
    echo "🌐 Access the application at:"
    echo "   Frontend: http://localhost:3000"
    echo "   Backend API: http://localhost:8000"
    echo "   API Docs: http://localhost:8000/docs"
    echo ""
    echo "📊 View logs with: $COMPOSE_CMD logs -f"
    echo "🛑 Stop with: $COMPOSE_CMD down"
else
    echo ""
    echo "❌ Some services failed to start. Check logs with:"
    echo "   $COMPOSE_CMD logs"
fi
