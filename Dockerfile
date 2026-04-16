# Institutional Build Refresh - Python 3.11
# Use Python 3.11 slim as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./backend/

# Start command using the recommended list form for better signal handling
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]
