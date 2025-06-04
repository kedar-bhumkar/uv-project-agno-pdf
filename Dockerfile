# Use Python 3.12 slim image as base
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy project files needed for installation
COPY pyproject.toml uv.lock README.md ./

# Install Python dependencies
RUN pip install --no-cache-dir uv && \
    uv venv && \
    . .venv/bin/activate && \
    uv pip install --no-cache-dir "fastapi[standard]" uvicorn && \
    uv pip install --no-cache-dir .

# Copy the rest of the application
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

# Expose port if needed (adjust if your app uses a different port)
EXPOSE 8000

# Command to run the application
CMD ["uv", "run", "uvicorn", "apps.main:app", "--host", "0.0.0.0", "--port", "8000"] 