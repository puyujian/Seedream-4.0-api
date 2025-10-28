#!/bin/bash

set -e

echo "🔨 Building Docker Images for Volcengine Image Generator"
echo "========================================================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

print_success "Docker is running"

# Check if docker compose is available (V2 or V1)
if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
elif docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
else
    echo "❌ docker compose is not available. Please install Docker Compose and try again."
    exit 1
fi

print_success "Docker Compose is available ($COMPOSE_CMD)"

echo ""
print_info "Building backend image..."
$COMPOSE_CMD build --no-cache backend

echo ""
print_info "Building frontend image (this may take a while)..."
$COMPOSE_CMD build --no-cache frontend

echo ""
print_success "All images built successfully!"

echo ""
echo "📋 Built images:"
docker images | grep -E "volcengine-|IMAGE" || echo "   No volcengine images found yet"

echo ""
echo "🎯 Next steps:"
echo "   1. Run './scripts/test-build.sh' to test the build"
echo "   2. Run 'docker-compose up -d' to start the services"
echo "   3. Run './scripts/start.sh' for automated startup"
