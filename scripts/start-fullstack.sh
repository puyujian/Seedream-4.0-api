#!/bin/bash

set -e

echo "🚀 Starting Volcengine Image Generator (Fullstack Single Image)"
echo "==============================================================="

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
echo "📦 Building fullstack Docker image..."
$COMPOSE_CMD -f docker-compose.fullstack.yml build

echo ""
echo "🎬 Starting fullstack service..."
$COMPOSE_CMD -f docker-compose.fullstack.yml up -d

echo ""
echo "⏳ Waiting for service to be ready..."
sleep 10

# Check if service is running
if $COMPOSE_CMD -f docker-compose.fullstack.yml ps | grep -q "Up"; then
    echo ""
    echo "✅ Application started successfully!"
    echo ""
    echo "🌐 Access the application at:"
    echo "   Application: http://localhost:3000"
    echo "   Backend API: http://localhost:3000/api"
    echo "   Health Check: http://localhost:3000/health"
    echo ""
    echo "📊 View logs with:"
    echo "   All logs: $COMPOSE_CMD -f docker-compose.fullstack.yml logs -f"
    echo "   Backend logs: docker exec volcengine-app tail -f /var/log/supervisor/uvicorn.log"
    echo "   Nginx logs: docker exec volcengine-app tail -f /var/log/supervisor/nginx.log"
    echo ""
    echo "🛑 Stop with: $COMPOSE_CMD -f docker-compose.fullstack.yml down"
else
    echo ""
    echo "❌ Service failed to start. Check logs with:"
    echo "   $COMPOSE_CMD -f docker-compose.fullstack.yml logs"
fi
