FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application
COPY reddit_cli.py .
COPY README.md .

# Create a volume for configuration
VOLUME ["/app/config"]

# Make the script executable
RUN chmod +x reddit_cli.py

# Set the default command
ENTRYPOINT ["python", "reddit_cli.py"]
CMD ["--help"]
