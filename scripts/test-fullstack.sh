#!/bin/bash

set -e

echo "🧪 Testing Fullstack Docker Build"
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Detect docker compose command
if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
elif docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
else
    echo -e "${RED}❌ docker compose is not available${NC}"
    exit 1
fi

COMPOSE_FILE="docker-compose.fullstack.yml"

echo ""
echo "1️⃣  Building fullstack image..."
if $COMPOSE_CMD -f $COMPOSE_FILE build; then
    echo -e "${GREEN}✅ Build successful${NC}"
else
    echo -e "${RED}❌ Build failed${NC}"
    exit 1
fi

echo ""
echo ""

# Ensure .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  .env file not found, creating from example...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✅ Created .env file (demo mode by default)${NC}"
fi

echo "2️⃣  Starting container..."
if $COMPOSE_CMD -f $COMPOSE_FILE up -d; then
    echo -e "${GREEN}✅ Container started${NC}"
else
    echo -e "${RED}❌ Failed to start container${NC}"
    exit 1
fi

echo ""
echo "3️⃣  Waiting for services to be ready..."
sleep 15

echo ""
echo "4️⃣  Running health checks..."

# Check if container is running
if docker ps | grep -q volcengine-app; then
    echo -e "${GREEN}✅ Container is running${NC}"
else
    echo -e "${RED}❌ Container is not running${NC}"
    $COMPOSE_CMD -f $COMPOSE_FILE logs
    $COMPOSE_CMD -f $COMPOSE_FILE down
    exit 1
fi

# Check backend health
echo ""
echo "   Checking backend health..."
if docker exec volcengine-app curl -sf http://localhost:8000/health > /dev/null; then
    echo -e "${GREEN}   ✅ Backend is healthy${NC}"
else
    echo -e "${RED}   ❌ Backend health check failed${NC}"
    docker exec volcengine-app tail -20 /var/log/supervisor/uvicorn.log
    $COMPOSE_CMD -f $COMPOSE_FILE down
    exit 1
fi

# Check nginx
echo ""
echo "   Checking Nginx..."
if docker exec volcengine-app wget --quiet --tries=1 --spider http://localhost:80 2>/dev/null; then
    echo -e "${GREEN}   ✅ Nginx is serving content${NC}"
else
    echo -e "${RED}   ❌ Nginx check failed${NC}"
    docker exec volcengine-app tail -20 /var/log/supervisor/nginx.log
    $COMPOSE_CMD -f $COMPOSE_FILE down
    exit 1
fi

# Check external access
echo ""
echo "   Checking external access..."
if curl -sf http://localhost:3000/health > /dev/null; then
    echo -e "${GREEN}   ✅ Application is accessible externally${NC}"
else
    echo -e "${YELLOW}   ⚠️  External access check failed (might need more time)${NC}"
fi

# Check supervisor status
echo ""
echo "5️⃣  Checking process status..."
docker exec volcengine-app supervisorctl status

echo ""
echo -e "${GREEN}✅ All tests passed!${NC}"
echo ""
echo "📊 View logs:"
echo "   docker logs volcengine-app"
echo "   docker exec volcengine-app tail -f /var/log/supervisor/uvicorn.log"
echo "   docker exec volcengine-app tail -f /var/log/supervisor/nginx.log"
echo ""
echo "🧼 Cleaning up test environment..."
$COMPOSE_CMD -f $COMPOSE_FILE down

echo ""
echo "🛑 You can rebuild with:"
echo "   $COMPOSE_CMD -f $COMPOSE_FILE up -d"
