# Stage 1: Builder
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim as builder

# Set environment variables for uv
ENV UV_NO_HARDLINKS=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /app

# Copy project files and lock file
COPY pyproject.toml uv.lock ./

# Sync dependencies using uv --locked
RUN uv sync --no-dev --locked

# Stage 2: Runtime
FROM python:3.12-slim-bookworm

WORKDIR /app

# Copy the virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY src/ ./src/

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/app/src:$PYTHONPATH"

# Expose the port your Flask app listens on
EXPOSE 8000

# Command to run the Flask application using Gunicorn (WSGI server for Flask)
CMD ["gunicorn", "src.main:app", "--bind", "0.0.0.0:8000", "--workers", "4", "--threads", "2", "--timeout", "60"]