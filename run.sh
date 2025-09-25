#!/bin/bash

# Reddit CLI Docker Runner Script

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if config file exists
if [ ! -f "reddit_config.json" ]; then
    echo "❌ Configuration file not found!"
    echo "   Please run ./setup.sh first to create the configuration template."
    exit 1
fi

# Check if image exists, build if not
if ! docker image inspect reddit-cli > /dev/null 2>&1; then
    echo "🔨 Building Reddit CLI Docker image..."
    docker build -t reddit-cli .
fi

# Run the Reddit CLI with Docker
docker run --rm \
    -v "$(pwd)/reddit_config.json:/app/reddit_config.json" \
    reddit-cli "$@"
