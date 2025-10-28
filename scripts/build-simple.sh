#!/bin/bash

set -e

echo "🔨 Simple Docker Build for Volcengine Image Generator"
echo "======================================================"

# Detect docker compose command
if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
elif docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
else
    echo "❌ docker compose is not available"
    exit 1
fi

echo "✅ Using: $COMPOSE_CMD"
echo ""

# Build with cache to speed up
echo "📦 Building images (with cache)..."
$COMPOSE_CMD build

echo ""
echo "✅ Build completed!"
echo ""
echo "📋 Images:"
docker images | grep volcengine || echo "   No volcengine images found yet"
