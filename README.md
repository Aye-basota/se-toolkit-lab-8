# AI Agent Interface for LMS

An AI agent interface (Nanobot-style) that turns a Learning Management System into a conversational experience. Users ask questions in natural language and the agent calls tools to fetch data from the backend and observability stack.

## Features

- Natural language interface to LMS data
- MCP tools for LMS queries and log/trace analysis
- WebSocket + Flutter web chat client
- Scheduled health checks and proactive alerts
- Observability integration (OpenTelemetry, VictoriaLogs, VictoriaTraces)

## Tech stack

- Python, FastAPI
- Nanobot agent framework
- MCP (Model Context Protocol) tools
- Flutter Web, WebSocket
- Docker, Docker Compose
- OpenTelemetry, VictoriaLogs, VictoriaTraces

## Quick start

```bash
docker compose up --build
```

## Architecture

- `backend/` — LMS API
- `nanobot/` — Agent core
- `client-web-react/` — Web chat UI
- `mcp/` — Tool definitions
