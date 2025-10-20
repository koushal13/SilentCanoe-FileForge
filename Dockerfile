FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libreoffice \
    tesseract-ocr \
    tesseract-ocr-eng \
    pandoc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install the package
RUN pip install -e .

# Create non-root user
RUN useradd -m -u 1000 fileforge && \
    chown -R fileforge:fileforge /app
USER fileforge

# Expose port for GUI (if running web interface in future)
EXPOSE 8080

# Set default command
CMD ["python", "fileforge.py", "--help"]

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import fileforge; print('OK')" || exit 1

# Labels
LABEL org.opencontainers.image.title="SilentCanoe FileForge"
LABEL org.opencontainers.image.description="Universal File Conversion Toolkit"
LABEL org.opencontainers.image.source="https://github.com/silentcanoe/fileforge"
LABEL org.opencontainers.image.vendor="SilentCanoe"
LABEL org.opencontainers.image.licenses="MIT"