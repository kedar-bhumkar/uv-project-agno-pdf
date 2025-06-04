# Agno PDF Agent

A Python-based PDF processing agent built with FastAPI.

## Features

- PDF processing capabilities
- FastAPI web interface
- Integration with various AI/ML services

## Installation

```bash
# Build the Docker image
docker build -t agno-pdf-agent .

# Run the container
docker run -p 8000:8000 agno-pdf-agent
```

## Development

The project uses Python 3.12 and can be run locally using:

```bash
uv run uvicorn apps.main:app --reload
```
