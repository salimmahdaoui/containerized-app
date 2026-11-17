
# Base image
FROM python:3.12-slim

# Working directory
WORKDIR /app

# Python environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create a dedicated non-root user
RUN groupadd --system app \
    && useradd --system \
        --gid app \
        --no-create-home \
        --shell /usr/sbin/nologin \
        app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY --chown=app:app app ./app

# Run as non-root user
USER app

# Application port
EXPOSE 8000

# Start FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

