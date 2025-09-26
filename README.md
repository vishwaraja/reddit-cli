# Reddit CLI Tool

> 🚀 **A comprehensive command-line interface for Reddit** - Post, comment, vote, search, and manage your Reddit presence from the terminal with professional-grade features and beautiful output.

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
[![Docker Hub](https://img.shields.io/badge/docker%20hub-vishwa86%2Freddit--cli-blue.svg)](https://hub.docker.com/r/vishwa86/reddit-cli)
[![Open Source](https://img.shields.io/badge/Open%20Source-Yes-green.svg)](https://github.com/vishwaraja/reddit-cli)

A powerful, feature-rich command-line tool for interacting with Reddit. From posting content and engaging with communities to managing your Reddit presence, this tool provides everything you need to be productive on Reddit from your terminal.

> 📖 **Read the full story**: [Building a Comprehensive Reddit CLI Tool: From Basic Posting to Full Reddit Management](https://dev.to/vishwaraja_pathivishwa/building-a-comprehensive-reddit-cli-tool-from-basic-posting-to-full-reddit-management-with-33-533f) on Dev.to

## 🚀 Features

* **📝 Complete Content Management**: Post, edit, delete, and manage your Reddit content
* **💬 Advanced Commenting**: Comment, reply, and engage with Reddit communities
* **🔍 Powerful Search**: Search posts, comments, and subreddits across Reddit
* **👥 User Management**: View profiles, follow users, and manage relationships
* **📊 Content Discovery**: Find trending subreddits and hot posts
* **💾 Content Organization**: Save, unsave, and organize your Reddit content
* **📬 Messaging System**: Send and receive private messages
* **🗳️ Voting System**: Upvote and downvote posts and comments
* **🏷️ Flair Support**: Use subreddit flairs for better categorization
* **🛡️ Rate Limiting**: Built-in rate limiting and error handling
* **🐳 Docker Ready**: Easy deployment with Docker containers
* **📱 Beautiful Output**: Professional, emoji-rich terminal output

## 📦 Installation

### Option 1: Docker Hub (Easiest - Recommended)

```bash
# Pull the image from Docker Hub
docker pull vishwa86/reddit-cli:latest

# Create a configuration directory
mkdir -p ~/.reddit-cli
cd ~/.reddit-cli

# Create your configuration file
cat > reddit_config.json << EOF
{
  "client_id": "your_client_id_here",
  "client_secret": "your_client_secret_here", 
  "username": "your_reddit_username",
  "password": "your_reddit_password",
  "user_agent": "RedditCLI/2.0 by your_username"
}
EOF

# Run the CLI
docker run --rm -v ~/.reddit-cli/reddit_config.json:/app/reddit_config.json vishwa86/reddit-cli:latest --help
```

### Option 2: Local Docker Setup

```bash
# Clone the repository
git clone https://github.com/vishwaraja/reddit-cli.git
cd reddit-cli

# Run the setup script
./setup.sh

# Configure your Reddit API credentials
cp reddit_config.json.example reddit_config.json
# Edit reddit_config.json with your credentials
```

### Option 3: Direct Installation

```bash
# Clone the repository
git clone https://github.com/vishwaraja/reddit-cli.git
cd reddit-cli

# Install dependencies
pip install -r requirements.txt

# Configure your Reddit API credentials
cp reddit_config.json.example reddit_config.json
# Edit reddit_config.json with your credentials
```

## 🔧 Reddit API Setup

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

## 📖 Usage

### Quick Start

#### Using Docker Hub (Recommended)
```bash
# Check all available commands
docker run --rm -v ~/.reddit-cli/reddit_config.json:/app/reddit_config.json vishwa86/reddit-cli:latest --help

# Post to a subreddit
docker run --rm -v ~/.reddit-cli/reddit_config.json:/app/reddit_config.json vishwa86/reddit-cli:latest post askreddit "What's your favorite programming language?" --content "I'm curious about what developers prefer and why."

# Search for subreddits
docker run --rm -v ~/.reddit-cli/reddit_config.json:/app/reddit_config.json vishwa86/reddit-cli:latest search-subreddits "programming" --limit 10

# Get user profile
docker run --rm -v ~/.reddit-cli/reddit_config.json:/app/reddit_config.json vishwa86/reddit-cli:latest user-profile "spez"

# Search for posts
docker run --rm -v ~/.reddit-cli/reddit_config.json:/app/reddit_config.json vishwa86/reddit-cli:latest search-posts "Python tutorial" --subreddit "learnpython" --limit 5
```

#### Using Local Setup
```bash
# Check all available commands
./run.sh --help

# Post to a subreddit
./run.sh post askreddit "What's your favorite programming language?" --content "I'm curious about what developers prefer and why."

# Search for subreddits
./run.sh search-subreddits "programming" --limit 10

# Get user profile
./run.sh user-profile "spez"

# Search for posts
./run.sh search-posts "Python tutorial" --subreddit "learnpython" --limit 5
```

### Content Management

#### Posting Content

```bash
# Text Post
./run.sh post askreddit "What's the best way to learn Python?" --content "I'm a beginner looking for effective learning resources and tips."

# Link Post
./run.sh post programming "Amazing Python library" --url "https://github.com/pandas-dev/pandas"

# Post with Flair
./run.sh flairs programming  # Get available flairs first
./run.sh post programming "Python Data Analysis" --content "Great resources for data analysis" --flair "flair_id_here"
```

#### Commenting and Engagement

```bash
# Comment on a post
./run.sh comment "https://reddit.com/r/askreddit/comments/abc123/post/" "Great question! I think Python is excellent for beginners."

# Reply to a comment
./run.sh reply "https://reddit.com/r/askreddit/comments/abc123/post/comment_id/" "I agree with your point about Python's simplicity."

# Upvote/Downvote
./run.sh upvote "https://reddit.com/r/askreddit/comments/abc123/post/"
./run.sh downvote "https://reddit.com/r/askreddit/comments/abc123/post/"
```

### Content Discovery

#### Subreddit Management

```bash
# Search for subreddits
./run.sh search-subreddits "machine learning" --limit 10

# Get subreddit information
./run.sh subreddit-info "MachineLearning"

# Subscribe to subreddits
./run.sh subscribe "MachineLearning"
./run.sh unsubscribe "MachineLearning"

# Get trending subreddits
./run.sh trending --limit 10

# Get subreddit moderators
./run.sh moderators "MachineLearning"
```

#### Content Search

```bash
# Search posts across Reddit
./run.sh search-posts "Python tutorial" --limit 10

# Search posts in specific subreddit
./run.sh search-posts "data science" --subreddit "MachineLearning" --limit 5

# Search comments
./run.sh search-comments "help" --subreddit "learnpython" --limit 5

# Get hot posts
./run.sh hot "programming" --limit 10
```

### User Management

#### User Profiles and History

```bash
# Get user profile
./run.sh user-profile "spez"

# Get user's posts
./run.sh user-posts "spez" --limit 10

# Get user's comments
./run.sh user-comments "spez" --limit 10

# Follow/Unfollow users
./run.sh follow "username"
./run.sh unfollow "username"

# Get friends list
./run.sh friends
```

### Content Organization

#### Save and Manage Content

```bash
# Save posts for later
./run.sh save "https://reddit.com/r/askreddit/comments/abc123/post/"

# Get saved posts
./run.sh saved-posts --limit 10

# Unsave posts
./run.sh unsave "https://reddit.com/r/askreddit/comments/abc123/post/"
```

### Messaging

#### Private Messaging

```bash
# Send private message
./run.sh message "username" "Subject" "Message body"

# Get inbox messages
./run.sh inbox --limit 10
```

### Content Editing

#### Edit Posts and Comments

```bash
# Edit your posts
./run.sh edit-post "https://reddit.com/r/askreddit/comments/abc123/post/" "Updated content"

# Edit your comments
./run.sh edit-comment "https://reddit.com/r/askreddit/comments/abc123/post/comment_id/" "Updated comment"
```

### Monitoring and Analytics

#### Monitor Posts

```bash
# Monitor post for new responses
./run.sh monitor "https://reddit.com/r/askreddit/comments/abc123/post/" --interval 60 --max-checks 5

# Get post responses
./run.sh responses "https://reddit.com/r/askreddit/comments/abc123/post/" --limit 20
```

## 📊 Command Reference

### Content Management Commands

| Command | Description | Example |
|---------|-------------|---------|
| `post` | Post to a subreddit | `./run.sh post askreddit "Title" --content "Content"` |
| `comment` | Comment on a post | `./run.sh comment "post_url" "comment_text"` |
| `reply` | Reply to a comment | `./run.sh reply "comment_url" "reply_text"` |
| `edit-post` | Edit a post | `./run.sh edit-post "post_url" "new_content"` |
| `edit-comment` | Edit a comment | `./run.sh edit-comment "comment_url" "new_content"` |
| `delete` | Delete a post | `./run.sh delete "post_url"` |

### Voting Commands

| Command | Description | Example |
|---------|-------------|---------|
| `upvote` | Upvote post/comment | `./run.sh upvote "post_url"` |
| `downvote` | Downvote post/comment | `./run.sh downvote "post_url"` |

### Discovery Commands

| Command | Description | Example |
|---------|-------------|---------|
| `search-subreddits` | Search for subreddits | `./run.sh search-subreddits "query" --limit 10` |
| `search-posts` | Search for posts | `./run.sh search-posts "query" --subreddit "subreddit"` |
| `search-comments` | Search for comments | `./run.sh search-comments "query" --limit 5` |
| `hot` | Get hot posts | `./run.sh hot "subreddit" --limit 10` |
| `trending` | Get trending subreddits | `./run.sh trending --limit 10` |

### User Management Commands

| Command | Description | Example |
|---------|-------------|---------|
| `user-profile` | Get user profile | `./run.sh user-profile "username"` |
| `user-posts` | Get user's posts | `./run.sh user-posts "username" --limit 10` |
| `user-comments` | Get user's comments | `./run.sh user-comments "username" --limit 10` |
| `follow` | Follow a user | `./run.sh follow "username"` |
| `unfollow` | Unfollow a user | `./run.sh unfollow "username"` |
| `friends` | Get friends list | `./run.sh friends` |

### Subreddit Management Commands

| Command | Description | Example |
|---------|-------------|---------|
| `subreddit-info` | Get subreddit info | `./run.sh subreddit-info "subreddit"` |
| `subscribe` | Subscribe to subreddit | `./run.sh subscribe "subreddit"` |
| `unsubscribe` | Unsubscribe from subreddit | `./run.sh unsubscribe "subreddit"` |
| `moderators` | Get subreddit moderators | `./run.sh moderators "subreddit"` |
| `flairs` | Get available flairs | `./run.sh flairs "subreddit"` |

### Content Organization Commands

| Command | Description | Example |
|---------|-------------|---------|
| `save` | Save a post | `./run.sh save "post_url"` |
| `unsave` | Unsave a post | `./run.sh unsave "post_url"` |
| `saved-posts` | Get saved posts | `./run.sh saved-posts --limit 10` |

### Messaging Commands

| Command | Description | Example |
|---------|-------------|---------|
| `message` | Send private message | `./run.sh message "username" "subject" "body"` |
| `inbox` | Get inbox messages | `./run.sh inbox --limit 10` |

### Monitoring Commands

| Command | Description | Example |
|---------|-------------|---------|
| `monitor` | Monitor post responses | `./run.sh monitor "post_url" --interval 60` |
| `responses` | Get post responses | `./run.sh responses "post_url" --limit 10` |

## 🎯 Use Cases

### Content Creators
- **Automated Posting**: Schedule and manage content across multiple subreddits
- **Community Engagement**: Monitor responses and engage with your audience
- **Content Research**: Find trending topics and popular discussions

### Developers
- **Project Promotion**: Share your open-source projects with relevant communities
- **Technical Discussions**: Participate in programming and tech subreddits
- **Learning Resources**: Find and share educational content

### Researchers
- **Data Collection**: Gather insights from Reddit discussions
- **Trend Analysis**: Monitor trending topics and community sentiment
- **Academic Research**: Study online communities and social behavior

### Business Users
- **Brand Management**: Monitor mentions and engage with customers
- **Market Research**: Understand customer needs and preferences
- **Community Building**: Build and nurture online communities

## 🔧 Technical Details

* **API Integration**: Uses PRAW (Python Reddit API Wrapper) for robust Reddit API access
* **Rate Limiting**: Built-in exponential backoff and retry logic
* **Error Handling**: Comprehensive error handling with user-friendly messages
* **Docker Support**: Containerized deployment for easy setup
* **Cross-Platform**: Works on macOS, Linux, and Windows
* **Configuration**: JSON-based configuration with secure credential management

## 🧪 Testing

```bash
# Run tests (if available)
python -m pytest tests/

# Test specific functionality
./run.sh --help  # Test help system
./run.sh trending --limit 3  # Test API connectivity
```

## 📁 Project Structure

```
reddit-cli/
├── reddit_cli.py              # Main CLI application
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker configuration
├── setup.sh                   # Setup script
├── run.sh                     # Run script
├── README.md                  # This file
├── LICENSE                    # MIT License
├── .gitignore                 # Git ignore rules
└── reddit_config.json.example # Configuration template
```

## 🤝 Contributing

We welcome contributions! Please see our Contributing Guide for details.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/vishwaraja/reddit-cli.git
cd reddit-cli

# Install dependencies
pip install -r requirements.txt

# Make your changes and test
./run.sh --help
```

### Contributing Guidelines

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

* **GitHub Issues**: Report bugs or request features
* **Email**: vishwaraja.pathi@adiyogitech.com
* **Documentation**: Check this README for usage examples

## 📖 Related Content

* **Technical Article**: [Building a Comprehensive Reddit CLI Tool: From Basic Posting to Full Reddit Management](https://dev.to/vishwaraja_pathivishwa/building-a-comprehensive-reddit-cli-tool-from-basic-posting-to-full-reddit-management-with-33-533f)
* **Author**: @vishwaraja_pathivishwa on Dev.to

## 🔄 Version History

* **v1.0.0** - Initial release with basic posting functionality
* **v1.1.0** - Added commenting and flair support
* **v1.2.0** - Added subreddit discovery and management
* **v2.0.0** - Complete Reddit API implementation with 33+ commands

## ⚠️ Important Notes

- **Rate Limits**: Reddit has strict rate limits. The tool includes automatic delays to comply with Reddit's rules.
- **Subreddit Rules**: Always follow the rules of the subreddits you're posting to.
- **API Limits**: Be mindful of Reddit's API usage limits and terms of service.
- **Security**: Keep your `reddit_config.json` file secure and never share it publicly.
- **Privacy**: This tool is completely generic and doesn't store or track any of your Reddit activity or content.
- **Responsible Use**: Use the tool responsibly and in accordance with Reddit's terms of service.

## 🎉 Acknowledgments

- Built with [PRAW](https://praw.readthedocs.io/) - Python Reddit API Wrapper
- Docker support for easy deployment
- Inspired by the need for a comprehensive Reddit CLI tool
- Community feedback and contributions

---

_Made with ❤️ for the Reddit community_

## About

A comprehensive command-line interface for Reddit that provides professional-grade features for content management, community engagement, and Reddit automation.

### Resources

- [Reddit API Documentation](https://praw.readthedocs.io/)
- [Reddit App Preferences](https://www.reddit.com/prefs/apps)
- [Reddit Terms of Service](https://www.redditinc.com/policies/user-agreement)

### License

MIT License - see [LICENSE](LICENSE) file for details.

### Contributing

Contributions are welcome! Please see our Contributing Guide above.

---

**⭐ Star this repository if you find it useful!**