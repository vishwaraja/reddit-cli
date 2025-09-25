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

# Run the Reddit CLI with Docker
docker-compose run --rm reddit-cli "$@"
