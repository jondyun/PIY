# Base image
FROM python:3.10-slim

# Set workdir
WORKDIR /app

# Install system dependencies for SuperSlicer
RUN apt-get update && apt-get install -y \
    libgtk-3-0 \
    libglu1-mesa \
    libgl1 \
    libglib2.0-0 \
    libxcb1 \
    && rm -rf /var/lib/apt/lists/*

# Copy SuperSlicer archive
COPY SuperSlicer.tgz /tmp/SuperSlicer.tgz

# Extract SuperSlicer
RUN mkdir -p /opt/superslicer && \
    tar -xvzf /tmp/SuperSlicer.tgz -C /opt/superslicer --strip-components=1 && \
    rm /tmp/SuperSlicer.tgz

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app and config
COPY app.py .
COPY config.ini /app/config.ini

# Copy frontend
COPY frontend /app/frontend

# Expose port
EXPOSE 8080

# Run app
CMD ["python", "app.py"]