# VERIFAI - Multimodal Misinformation Verifier (BAI-12)
# Production Containerized Deployment for Capstone Project
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies required for OpenCV and image processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY Backend/requirements.txt /app/Backend/requirements.txt
RUN pip install --no-cache-dir -r /app/Backend/requirements.txt truststore

# Copy codebase
COPY . /app

EXPOSE 5000

ENV PYTHONUNBUFFERED=1

WORKDIR /app/Backend
CMD ["python", "app.py"]
