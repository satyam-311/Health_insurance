# Use slim Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Prevent python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Prevent python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for layer caching)
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port
EXPOSE 8000

# Start API
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
