# Contributing to Reddit CLI

Thank you for your interest in contributing to the Reddit CLI project! This document provides guidelines and instructions for contributors.

## 🚀 Quick Start for Contributors

### Prerequisites
- Docker installed on your system
- Git installed
- A GitHub account
- Reddit API credentials (for testing)

### 1. Fork and Clone
```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/reddit-cli.git
cd reddit-cli
```

### 2. Set Up Development Environment
```bash
# Build the Docker image locally
docker build -t reddit-cli:dev .

# Create configuration for testing
mkdir -p ~/.reddit-cli
cp reddit_config.json.example ~/.reddit-cli/reddit_config.json
# Edit ~/.reddit-cli/reddit_config.json with your Reddit API credentials
```

### 3. Test Your Changes
```bash
# Test the CLI with your changes
docker run --rm -v ~/.reddit-cli/reddit_config.json:/app/reddit_config.json reddit-cli:dev --help

# Test specific functionality
docker run --rm -v ~/.reddit-cli/reddit_config.json:/app/reddit_config.json reddit-cli:dev trending --limit 3
```

## 📋 Development Workflow

### Making Changes
1. **Create a feature branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** to the codebase
3. **Test your changes** thoroughly
4. **Update documentation** if needed
5. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

### Commit Message Guidelines
We follow conventional commit format:
- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `style:` - Code style changes
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

### Testing Requirements
Before submitting a PR, ensure:
- [ ] Your changes work with Docker
- [ ] All existing functionality still works
- [ ] New features are tested
- [ ] Documentation is updated
- [ ] Code follows the existing style

## 🔄 Pull Request Process

### 1. Create a Pull Request
1. Push your branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
2. Create a Pull Request on GitHub
3. Fill out the PR template with:
   - Description of changes
   - Testing performed
   - Screenshots (if applicable)

### 2. PR Review Process
- **Automated Checks**: CI/CD pipeline will run automatically
- **Code Review**: Maintainers will review your code
- **Testing**: Your changes will be tested in the CI environment
- **Docker Build**: New Docker image will be built and tested

### 3. Merge Process
Once approved:
- **Squash and Merge**: Your PR will be squashed into a single commit
- **Automatic Deployment**: CI/CD will automatically:
  - Build new Docker image
  - Push to Docker Hub (`vishwa86/reddit-cli`)
  - Tag with version number
  - Update `latest` tag

## 🐳 Docker Development

### Local Development with Docker
```bash
# Build development image
docker build -t reddit-cli:dev .

# Run with your config
docker run --rm -v ~/.reddit-cli/reddit_config.json:/app/reddit_config.json reddit-cli:dev [command]

# Run interactively for debugging
docker run -it --rm -v ~/.reddit-cli/reddit_config.json:/app/reddit_config.json reddit-cli:dev bash
```

### Testing Docker Changes
```bash
# Test specific commands
docker run --rm -v ~/.reddit-cli/reddit_config.json:/app/reddit_config.json reddit-cli:dev post test "Test Post" --content "Test content"

# Test help system
docker run --rm -v ~/.reddit-cli/reddit_config.json:/app/reddit_config.json reddit-cli:dev --help
```

## 🔧 CI/CD Pipeline

### Automatic Builds
The project uses GitHub Actions for CI/CD:

- **On Push to Main**: Builds and pushes to Docker Hub
- **On Pull Request**: Builds and tests (doesn't push)
- **On Tag**: Creates versioned releases

### Docker Hub Integration
- **Repository**: `vishwa86/reddit-cli`
- **Tags**: 
  - `latest` - Latest stable version
  - `v1.0.0` - Versioned releases
  - `main` - Latest from main branch

### Required GitHub Secrets
The following secrets must be configured in the repository:
- `DOCKER_USERNAME` - Docker Hub username
- `DOCKER_PASSWORD` - Docker Hub password/token

## 📝 Code Style Guidelines

### Python Code Style
- Follow PEP 8 guidelines
- Use type hints where appropriate
- Add docstrings for all functions
- Use meaningful variable names

### Error Handling
- Use try-catch blocks for API calls
- Provide user-friendly error messages
- Include emojis in output for better UX
- Log errors appropriately

### Documentation
- Update README.md for new features
- Add examples for new commands
- Update help text in the CLI
- Document any breaking changes

## 🐛 Reporting Issues

### Bug Reports
When reporting bugs, please include:
- **Description**: Clear description of the issue
- **Steps to Reproduce**: Detailed steps
- **Expected Behavior**: What should happen
- **Actual Behavior**: What actually happens
- **Environment**: Docker version, OS, etc.
- **Logs**: Any error messages or logs

### Feature Requests
For feature requests, please include:
- **Use Case**: Why this feature is needed
- **Proposed Solution**: How you think it should work
- **Alternatives**: Other solutions you've considered

## 🤝 Community Guidelines

### Code of Conduct
- Be respectful and inclusive
- Help others learn and grow
- Provide constructive feedback
- Follow the golden rule

### Getting Help
- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion
- **Email**: vishwaraja.pathi@adiyogitech.com

## 🎯 Areas for Contribution

### High Priority
- **Bug Fixes**: Fix any reported issues
- **Documentation**: Improve README and docs
- **Testing**: Add more comprehensive tests
- **Error Handling**: Improve error messages

### Medium Priority
- **New Features**: Add new Reddit API endpoints
- **Performance**: Optimize API calls
- **UI/UX**: Improve terminal output
- **Cross-platform**: Ensure Windows compatibility

### Low Priority
- **Web Interface**: Create a web UI
- **Mobile App**: Create a mobile version
- **Analytics**: Add usage analytics
- **Plugins**: Plugin system for extensions

## 📚 Resources

### Documentation
- [Reddit API Documentation](https://praw.readthedocs.io/)
- [Docker Documentation](https://docs.docker.com/)
- [GitHub Actions](https://docs.github.com/en/actions)

### Development Tools
- **Docker**: For containerized development
- **Git**: For version control
- **GitHub**: For collaboration
- **Docker Hub**: For image distribution

## 🏆 Recognition

Contributors will be recognized in:
- **README.md**: Contributors section
- **Release Notes**: For significant contributions
- **GitHub**: Contributor statistics

Thank you for contributing to Reddit CLI! 🚀
