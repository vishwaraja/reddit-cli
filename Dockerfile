FROM python:3.11-slim

# Set metadata
LABEL maintainer="vishwaraja.pathi@adiyogitech.com"
LABEL description="A comprehensive command-line interface for Reddit with 33+ commands"
LABEL version="2.0.0"
LABEL repository="https://github.com/vishwaraja/reddit-cli"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the application
COPY reddit_cli.py .
COPY README.md .

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash reddit \
    && chown -R reddit:reddit /app

# Create a volume for configuration
VOLUME ["/app/config"]

# Make the script executable
RUN chmod +x reddit_cli.py

# Switch to non-root user
USER reddit

# Set the default command
ENTRYPOINT ["python", "reddit_cli.py"]
CMD ["--help"]