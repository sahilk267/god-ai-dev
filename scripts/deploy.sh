#!/bin/bash

# Production Deployment Script for God-Level AI Developer System

set -e

echo "🚀 Deploying God-Level AI Developer System to Production..."

# Check prerequisites
command -v docker >/dev/null 2>&1 || { echo "Docker required but not installed. Aborting." >&2; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo "Docker Compose required but not installed. Aborting." >&2; exit 1; }

# Load environment variables
if [ -f .env.production ]; then
    export $(cat .env.production | grep -v '^#' | xargs)
fi

# Build and deploy
echo "📦 Building Docker images..."
docker-compose -f docker-compose.prod.yml build

echo "🔄 Stopping existing containers..."
docker-compose -f docker-compose.prod.yml down

echo "🚀 Starting production services..."
docker-compose -f docker-compose.prod.yml up -d

echo "✅ Deployment complete!"
echo "🌐 Application running at: http://localhost:80"
echo "📊 Check logs: docker-compose -f docker-compose.prod.yml logs -f"

# Health check
sleep 10
if curl -f http://localhost:8000/health; then
    echo "✅ Health check passed!"
else
    echo "⚠️ Health check failed. Check logs for details."
fi