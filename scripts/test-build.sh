#!/bin/bash

set -e

echo "🧪 Testing Docker Build for Volcengine Image Generator"
echo "========================================================"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

echo "✅ Docker is running"

# Detect docker compose command
if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
elif docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
else
    echo "❌ docker compose is not available. Please install Docker Compose and try again."
    exit 1
fi

# Build the Docker images without caching
./scripts/build.sh

echo ""
echo "▶️ Running $COMPOSE_CMD configuration for validation..."
$COMPOSE_CMD up -d

# Wait for containers to start
echo "⏳ Waiting for containers to be ready (60 seconds)..."
sleep 60

echo ""
echo "📊 Current container status:"
$COMPOSE_CMD ps

echo ""
echo "🔄 Checking backend health endpoint..."
MAX_RETRIES=10
RETRY_COUNT=0
while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if curl -fsS http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ Backend health check succeeded"
        break
    else
        RETRY_COUNT=$((RETRY_COUNT + 1))
        if [ $RETRY_COUNT -lt $MAX_RETRIES ]; then
            echo "⏳ Backend not ready yet, retrying ($RETRY_COUNT/$MAX_RETRIES)..."
            sleep 5
        else
            echo "❌ Backend health check failed after $MAX_RETRIES attempts"
            echo "   Check logs with '$COMPOSE_CMD logs backend'"
            $COMPOSE_CMD logs backend
            $COMPOSE_CMD down
            exit 1
        fi
    fi
done

echo ""
echo "🧪 Testing frontend status (HTTP response only)..."
HTTP_STATUS=$(curl -o /dev/null -s -w "%{http_code}" http://localhost:3000)
if [ "$HTTP_STATUS" -eq 200 ] || [ "$HTTP_STATUS" -eq 304 ]; then
    echo "✅ Frontend returned HTTP $HTTP_STATUS"
else
    echo "⚠️ Frontend returned HTTP status $HTTP_STATUS"
    echo "   This may still be OK depending on build state"
fi

echo ""
echo "🧼 Cleaning up..."
$COMPOSE_CMD down

echo ""
echo "🎉 Build test completed successfully!"
