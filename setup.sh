#!/bin/bash

# Reddit CLI Docker Setup Script

echo "🐳 Reddit CLI Docker Setup"
echo "=========================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "   Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

echo "✅ Docker is installed"

# Build the Docker image
echo "🔨 Building Docker image..."
docker build -t reddit-cli .

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully!"
else
    echo "❌ Failed to build Docker image"
    exit 1
fi

# Check if config file exists
if [ ! -f "reddit_config.json" ]; then
    echo "📝 Creating Reddit configuration template..."
    cp reddit_config.json.example reddit_config.json
    echo "✅ Configuration template created at reddit_config.json"
    echo ""
    echo "🔧 Next steps:"
    echo "1. Edit reddit_config.json with your Reddit API credentials"
    echo "2. Get your credentials from: https://www.reddit.com/prefs/apps"
    echo "3. Run: ./run.sh --help to see available commands"
else
    echo "✅ Configuration file already exists"
fi

echo ""
echo "🎉 Setup complete! You can now use the Reddit CLI with Docker."
echo ""
echo "📖 Usage examples:"
echo "  ./run.sh post askreddit 'What are the best resources for [topic]?'"
echo "  ./run.sh flairs [subreddit_name]"
echo "  ./run.sh responses 'https://reddit.com/r/askreddit/comments/abc123/post/'"
echo "  ./run.sh comment 'https://reddit.com/r/subreddit/comments/post/' 'Your comment'"
echo "  ./run.sh hot [subreddit_name]"
echo ""
echo "💡 Run './run.sh --help' for more information"
