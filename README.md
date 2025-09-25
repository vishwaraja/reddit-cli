# Reddit CLI Tool

A powerful command-line interface for posting to Reddit subreddits and retrieving responses. This tool allows you to interact with Reddit programmatically from your terminal.

## Features

- 🚀 **Post to Subreddits**: Create text or link posts to any subreddit
- 💬 **Get Responses**: Retrieve comments and responses from your posts
- 🔍 **Monitor Posts**: Continuously monitor posts for new responses
- 🏷️ **Flair Support**: List and use subreddit flairs when posting
- ⚙️ **Easy Configuration**: Simple JSON-based configuration
- 🛡️ **Error Handling**: Comprehensive error handling and user-friendly messages
- 🐳 **Docker Support**: Easy setup with Docker containers

## Quick Start with Docker (Recommended)

1. **Clone this repository**:
   ```bash
   git clone https://github.com/vishwaraja/reddit-cli.git
   cd reddit-cli
   ```

2. **Run the setup script**:
   ```bash
   ./setup.sh
   ```

3. **Configure your Reddit API credentials**:
   ```bash
   cp reddit_config.json.example reddit_config.json
   # Edit reddit_config.json with your credentials
   ```

4. **Start using the CLI**:
   ```bash
   ./run.sh --help
   ```

## Manual Installation (Alternative)

1. **Clone this repository**:
   ```bash
   git clone https://github.com/vishwaraja/reddit-cli.git
   cd reddit-cli
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your Reddit API credentials**:
   ```bash
   cp reddit_config.json.example reddit_config.json
   # Edit reddit_config.json with your credentials
   ```

## Reddit API Setup

Before using this tool, you need to set up Reddit API credentials:

1. **Go to Reddit App Preferences**: https://www.reddit.com/prefs/apps
2. **Click "Create App" or "Create Another App"**
3. **Fill in the form**:
   - **Name**: Any name (e.g., "My Reddit CLI")
   - **App type**: Select "script"
   - **Description**: Optional
   - **About URL**: Optional
   - **Redirect URI**: `http://localhost:8080` (required but not used)
4. **Click "Create app"**
5. **Note down your credentials**:
   - **Client ID**: The string under your app name (looks like `abc123def456`)
   - **Client Secret**: The "secret" field

## Configuration

1. **Run the tool once** to create a configuration template:
   ```bash
   python reddit_cli.py post test "Test Post"
   ```

2. **Edit the generated `reddit_config.json` file**:
   ```json
   {
     "client_id": "your_client_id_here",
     "client_secret": "your_client_secret_here",
     "username": "your_reddit_username",
     "password": "your_reddit_password",
     "user_agent": "RedditCLI/1.0 by your_username"
   }
   ```

3. **Replace the placeholder values** with your actual Reddit API credentials

## Usage

### Docker Usage (Recommended)

**Post to a Subreddit**:
```bash
# Text Post
./run.sh post askreddit "What's your favorite programming language?" --content "I'm curious about what programming languages developers prefer and why."

# Link Post
./run.sh post programming "Check out this cool project" --url "https://github.com/user/repo"

# With Flair
./run.sh post askreddit "What's your favorite programming language?" --content "I'm curious about what programming languages developers prefer and why." --flair "flair_id_here"
```

**Get Available Flairs**:
```bash
./run.sh flairs askreddit
```

**Get Responses from a Post**:
```bash
./run.sh responses "https://reddit.com/r/askreddit/comments/abc123/your_post_title/"
```

**Monitor a Post for New Responses**:
```bash
./run.sh monitor "https://reddit.com/r/askreddit/comments/abc123/your_post_title/" --interval 60 --max-checks 5
```

### Manual Usage (Alternative)

**Post to a Subreddit**:
```bash
# Text Post
python reddit_cli.py post askreddit "What's your favorite programming language?" --content "I'm curious about what programming languages developers prefer and why."

# Link Post
python reddit_cli.py post programming "Check out this cool project" --url "https://github.com/user/repo"

# With Flair
python reddit_cli.py post askreddit "What's your favorite programming language?" --content "I'm curious about what programming languages developers prefer and why." --flair "flair_id_here"
```

**Get Available Flairs**:
```bash
python reddit_cli.py flairs askreddit
```

**Get Responses from a Post**:
```bash
python reddit_cli.py responses "https://reddit.com/r/askreddit/comments/abc123/your_post_title/"
```

**Monitor a Post for New Responses**:
```bash
python reddit_cli.py monitor "https://reddit.com/r/askreddit/comments/abc123/your_post_title/" --interval 60 --max-checks 5
```

## Command Reference

### `post` - Post to a subreddit
- `subreddit`: Subreddit name (without r/)
- `title`: Post title
- `--content`: Post content (for text posts)
- `--url`: URL (for link posts)
- `--flair`: Flair ID

### `responses` - Get responses for a post
- `post_url`: Reddit post URL
- `--limit`: Number of responses to fetch (default: 10)

### `monitor` - Monitor a post for new responses
- `post_url`: Reddit post URL
- `--interval`: Check interval in seconds (default: 30)
- `--max-checks`: Maximum number of checks (default: 10)

### `flairs` - Get available flairs for a subreddit
- `subreddit`: Subreddit name (without r/)

## Examples

### Example 1: Post a Question and Monitor Responses
```bash
# Post a question
./run.sh post askreddit "What's the best way to learn Python?" --content "I'm a beginner and want to know the most effective learning path."

# Monitor for responses (check every 2 minutes, 5 times)
./run.sh monitor "https://reddit.com/r/askreddit/comments/abc123/whats_the_best_way_to_learn_python/" --interval 120 --max-checks 5
```

### Example 2: Share a Link with Flair
```bash
# First, check available flairs
./run.sh flairs programming

# Post with a specific flair
./run.sh post programming "Amazing Python library for data science" --url "https://github.com/pandas-dev/pandas" --flair "flair_id_from_above"
```

### Example 3: Get Recent Responses
```bash
./run.sh responses "https://reddit.com/r/askreddit/comments/abc123/your_post_title/" --limit 20
```

### Example 4: Explore Any Topic
```bash
# Post a question about any topic
./run.sh post askreddit "What are the best resources for learning [topic]?" --content "I'm looking for good resources and recommendations."

# Check flairs in relevant subreddits
./run.sh flairs [subreddit_name]
```

## Important Notes

- **Rate Limits**: Reddit has rate limits. The tool includes automatic delays to comply with Reddit's rules.
- **Subreddit Rules**: Always follow the rules of the subreddits you're posting to.
- **API Limits**: Be mindful of Reddit's API usage limits.
- **Security**: Keep your `reddit_config.json` file secure and never share it publicly.
- **Privacy**: This tool is completely generic and doesn't store or track any of your Reddit activity or content.
- **Generic Use**: The tool can be used for any topic or subreddit - it's not limited to any specific use case.

## Troubleshooting

### Common Issues

1. **"Error loading configuration"**: Make sure your `reddit_config.json` file exists and has valid credentials.

2. **"Invalid credentials"**: Double-check your client ID, client secret, username, and password.

3. **"Forbidden" errors**: You might not have permission to post to that subreddit, or the subreddit might have posting restrictions.

4. **"Rate limit exceeded"**: Wait a few minutes before trying again.

### Getting Help

- Check Reddit's API documentation: https://praw.readthedocs.io/
- Verify your Reddit app settings: https://www.reddit.com/prefs/apps
- Make sure your Reddit account has the necessary permissions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- Built with [PRAW](https://praw.readthedocs.io/) - Python Reddit API Wrapper
- Docker support for easy deployment
- Inspired by the need for a simple Reddit CLI tool
