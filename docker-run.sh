#!/bin/bash

# Reddit CLI Docker Hub Runner Script
# This script makes it easy to run the Reddit CLI from Docker Hub

# Configuration
DOCKER_IMAGE="vishwa86/reddit-cli:latest"
CONFIG_DIR="$HOME/.reddit-cli"
CONFIG_FILE="$CONFIG_DIR/reddit_config.json"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker first."
    exit 1
fi

# Check if config file exists
if [ ! -f "$CONFIG_FILE" ]; then
    print_warning "Configuration file not found at $CONFIG_FILE"
    print_status "Creating configuration directory..."
    mkdir -p "$CONFIG_DIR"
    
    print_status "Creating configuration template..."
    cat > "$CONFIG_FILE" << EOF
{
  "client_id": "your_client_id_here",
  "client_secret": "your_client_secret_here",
  "username": "your_reddit_username", 
  "password": "your_reddit_password",
  "user_agent": "RedditCLI/2.0 by your_username"
}
EOF
    
    print_warning "Please edit $CONFIG_FILE with your Reddit API credentials"
    print_status "Get your credentials from: https://www.reddit.com/prefs/apps"
    exit 1
fi

# Pull the latest image
print_status "Pulling latest Reddit CLI image..."
docker pull "$DOCKER_IMAGE"

if [ $? -eq 0 ]; then
    print_success "Image pulled successfully!"
else
    print_error "Failed to pull image. Check your internet connection."
    exit 1
fi

# Run the Reddit CLI with Docker
print_status "Running Reddit CLI..."
docker run --rm \
    -v "$CONFIG_FILE:/app/reddit_config.json" \
    "$DOCKER_IMAGE" "$@"
