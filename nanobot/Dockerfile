# Nanobot Gateway Dockerfile - Multi-stage build with uv

# ---
# Stage 1: Build the application
# ---

ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB}astral/uv:python3.14-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

# Omit development dependencies
ENV UV_NO_DEV=1

# Disable Python downloads
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Copy workspace from parent context
COPY --from=workspace pyproject.toml uv.lock /app/
COPY pyproject.toml /app/nanobot/pyproject.toml

# Sync nanobot dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-workspace --package nanobot

# Copy the rest of the nanobot project
COPY . /app/nanobot

# Copy mcp directory and install it
COPY --from=workspace mcp /app/mcp
WORKDIR /app/mcp
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --no-deps --editable .

# Copy nanobot-websocket-channel directory and install it
COPY --from=workspace nanobot-websocket-channel /app/nanobot-websocket-channel
WORKDIR /app/nanobot
RUN --mount=type=cache,target=/root/.cache/uv \
    uv add --editable /app/nanobot-websocket-channel

# ---
# Stage 2: Final runtime image
# ---

ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB}python:3.14.2-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8

# Create non-root user
RUN groupadd --system --gid 999 nonroot \
    && useradd --system --gid 999 --uid 999 --create-home nonroot

# Copy application from builder
COPY --from=builder --chown=nonroot:nonroot /app /app

# Set PATH to include venv
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/nanobot:/app/mcp"

# Create workspace directory
RUN mkdir -p /app/nanobot/workspace && chown -R nonroot:nonroot /app/nanobot/workspace

USER nonroot
WORKDIR /app

# Run the entrypoint script which resolves env vars and starts gateway
CMD ["python", "/app/nanobot/entrypoint.py"]
