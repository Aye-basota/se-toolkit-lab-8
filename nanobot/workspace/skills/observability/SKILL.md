---
nanobot:
  always: true
  description: "Use observability tools to investigate system health, errors, and traces"
---

# Observability Skill

**Available:** true

## Purpose

This skill teaches you how to use the observability MCP tools to investigate system health, find errors, and analyze traces.

## Available Tools

You have access to these observability tools via MCP:

| Tool | Description | Parameters |
|------|-------------|------------|
| `logs_search` | Search logs in VictoriaLogs using LogsQL | `query` (default "*"), `limit` (default 10, max 100) |
| `logs_error_count` | Count errors per service over a time window | `minutes` (default 60, max 1440) |
| `traces_list` | List recent traces for a service | `service` (default "Learning Management Service"), `limit` (default 10) |
| `traces_get` | Fetch a specific trace by ID | `trace_id` (required) |

## How to Use

### When the user asks "Any errors in the last hour?"

1. First call `logs_error_count` with `minutes=60` to get error counts per service
2. If errors are found, call `logs_search` with `query="severity:ERROR"` to get details
3. Summarize findings concisely - don't dump raw JSON

### When the user asks "What went wrong?" or "Check system health"

1. Search recent error logs: `logs_search(query="severity:ERROR", limit=10)`
2. If you find a trace_id in the logs, fetch the trace: `traces_get(trace_id="...")`
3. Look for patterns:
   - Database connection errors (`Name or service not known`, `connection refused`)
   - HTTP errors (404, 500, 503)
   - Timeout errors
4. Summarize the root cause concisely

### When the user asks about a specific service

1. Search logs for that service: `logs_search(query="service.name:SERVICE_NAME")`
2. List traces: `traces_list(service="SERVICE_NAME")`
3. Report findings

### LogsQL Query Examples

- `*` - All logs
- `error` - Logs containing "error"
- `severity:ERROR` - Only error-level logs
- `service.name:backend` - Logs from backend service
- `trace_id:abc123...` - Logs for a specific trace

## Response Formatting

- **Be concise**: Summarize findings in 2-3 sentences
- **Highlight key errors**: Quote the error message
- **Include trace correlation**: Mention trace_id if relevant
- **Don't dump JSON**: Extract the important information

## Example Interactions

### Example 1: "Any errors in the last hour?"

```
You: Call logs_error_count(minutes=60)
Response: "In the last 60 minutes:
- Learning Management Service: 5 errors
- Most errors occurred between 11:30-11:35 UTC
- Primary cause: database connection failures"
```

### Example 2: "What went wrong?"

```
You: Call logs_search(query="severity:ERROR", limit=5)
You: Find trace_id in results, call traces_get(trace_id="...")
Response: "The system is experiencing database connection failures:
- Error: '[Errno -2] Name or service not known'
- Affected service: Learning Management Service
- Root cause: PostgreSQL database is unreachable
- Trace ID: 7e2ea238... shows the full request flow"
```

### Example 3: "Show me recent backend logs"

```
You: Call logs_search(query="service.name:Learning Management Service", limit=10)
Response: "Here are the 10 most recent backend logs:
[Summarize key events - requests, auth, db queries]
No errors detected in recent logs."
```

## Limits

- VictoriaLogs retains logs for 7 days
- VictoriaTraces retains traces for 7 days
- If tools return errors, explain what went wrong clearly
- If no data is found, say so honestly rather than hallucinating
