#!/bin/bash

# ArmedMusic Docker Launcher
# This script helps you quickly start the bot with Docker

set -e

echo "🚀 ArmedMusic Docker Setup"
echo "=========================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "📝 .env file not found. Creating from template..."
    if [ -f "env.example" ]; then
        cp env.example .env
        echo "✅ Created .env file from template."
        echo "⚠️  Please edit .env file with your configuration before running the bot."
        echo "   Required: API_ID, API_HASH, BOT_TOKEN, OWNER_ID, MONGO_DB_URI"
        exit 1
    else
        echo "❌ env.example template not found."
        exit 1
    fi
fi

# Check if required environment variables are set
echo "🔍 Checking configuration..."

REQUIRED_VARS=("API_ID" "API_HASH" "BOT_TOKEN" "OWNER_ID")
MISSING_VARS=()

for var in "${REQUIRED_VARS[@]}"; do
    if ! grep -q "^${var}=" .env || grep "^${var}=" .env | grep -q "your_.*_here\|$"; then
        MISSING_VARS+=("$var")
    fi
done

if [ ${#MISSING_VARS[@]} -ne 0 ]; then
    echo "❌ Missing or incomplete configuration for: ${MISSING_VARS[*]}"
    echo "   Please edit .env file and fill in all required values."
    exit 1
fi

echo "✅ Configuration looks good!"

# Create necessary directories
mkdir -p sessions logs

# Start the bot
echo "🐳 Starting ArmedMusic with Docker Compose..."
if command -v docker-compose &> /dev/null; then
    docker-compose up -d
else
    docker compose up -d
fi

echo "✅ Bot started successfully!"
echo ""
echo "📊 Useful commands:"
echo "   View logs: docker-compose logs -f armedmusic"
echo "   Stop bot:  docker-compose down"
echo "   Restart:   docker-compose restart armedmusic"
echo ""
echo "🎵 Your bot should now be running!"
echo "   Check Telegram for your bot status."
