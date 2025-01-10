# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.4.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false

# Add Poetry to PATH
ENV PATH="$POETRY_HOME/bin:$PATH"

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        build-essential \
        libpq-dev \
        git \
    && rm -rf /var/lib/apt/lists/* \
    # Install Poetry
    && curl -sSL https://install.python-poetry.org | python3 -

# Copy project files
COPY pyproject.toml poetry.lock README.md ./
COPY teleAgent ./teleAgent
COPY tests ./tests
COPY alembic.ini ./
COPY main.py ./

# Install dependencies
RUN poetry install --no-dev --no-interaction

# Create required directories
RUN mkdir -p logs

# Create a non-root user
RUN useradd -m -u 1000 teleAgent && \
    chown -R teleAgent:teleAgent /app

# Switch to non-root user
USER teleAgent

# Expose port
EXPOSE 8000

# Set entrypoint
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]