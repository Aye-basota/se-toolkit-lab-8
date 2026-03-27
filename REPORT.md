# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

### Question 1: "What is the agentic loop?"

**Response:**
The agentic loop is the core architectural pattern that distinguishes AI agents from simple chatbots. It's an iterative execution cycle that enables autonomous, multi-step task completion.

**Key Concept:**
A chatbot is built to respond. An agent is built to act. The difference is one while loop.

**The 5-Stage Agent Loop:**
1. **Perceive** — Gather context from the environment, user input, and previous results
2. **Reason** — The LLM analyzes the situation and available options
3. **Plan** — Determine the next action or sequence of actions
4. **Act** — Execute tools, APIs, or other actions
5. **Observe** — Capture the outcome and feed it back into the next iteration

This cycle repeats until the task is complete or a stopping condition is reached.

### Question 2: "What labs are available in our LMS?"

**Response:**
The agent responded with information about Lab 8 from the README.md file in the workspace, describing the task structure and system architecture. However, it **cannot access real LMS backend data** because it has no tools configured yet. This demonstrates the limitation of a bare agent — it can only read files in its workspace, not query external APIs.

---

## Task 1B — Agent with LMS tools

### Question 1: "What labs are available in the LMS backend?"

**Response:**
The agent successfully called the `lms_labs` MCP tool and returned real data from the backend:

| ID | Lab     | Description            |
|----|---------|------------------------|
| 1  | lab-01  | Introduction to Python |
| 2  | lab-02  | Data Structures        |
| 3  | lab-03  | Algorithms             |

This demonstrates that the MCP server is correctly connected and the agent can discover and invoke tools.

### Question 2: "Describe the architecture of the LMS system"

**Response:**
The agent provided a comprehensive architecture description including:
- **Architecture diagram** showing clients (React, Flutter, Telegram) → Caddy Gateway → Nanobot Agent → LMS Backend → PostgreSQL
- **Observability stack**: OTel Collector → VictoriaLogs/VictoriaTraces
- **Core services table** with technologies and ports
- **Backend API structure** with routers for items, learners, interactions, pipeline, analytics
- **Data model** and deployment model

The agent synthesized information from both the workspace files AND the MCP tools to provide a complete answer.

---

## Task 1C — Skill prompt

### Test: "Show me the scores" (without specifying a lab)

**Response:**
The agent used the LMS skill to provide a comprehensive response:

1. First checked system health with `lms_health`
2. Called `lms_labs` to get available labs
3. Called `lms_completion_rate` for each lab
4. Presented results in a formatted table:

| Lab     | Description            | Completion Rate | Passed | Total |
|---------|------------------------|-----------------|--------|-------|
| lab-01  | Introduction to Python | 0.0%            | 0      | 0     |
| lab-02  | Data Structures        | 0.0%            | 0      | 0     |
| lab-03  | Algorithms             | 0.0%            | 0      | 0     |

The skill prompt successfully guides the agent to:
- Check system health first
- List available labs when no specific lab is mentioned
- Format numeric results as percentages
- Present data in tables
- Offer follow-up actions

**Skill file:** `nanobot/workspace/skills/lms/SKILL.md`

---

## Task 2A — Deployed agent

### Nanobot Gateway Startup Logs

```
nanobot-1  | Using config: /tmp/nanobot-config-resolved.json
nanobot-1  | 🐈 Starting nanobot gateway version 0.1.4.post5 on port 18790...
nanobot-1  | 2026-03-27 10:59:30.450 | DEBUG | nanobot.agent.tools.mcp:connect_mcp_servers:162 - MCP: registered tool 'mcp_lms_lms_health' from server 'lms'
nanobot-1  | 2026-03-27 10:59:30.450 | DEBUG | nanobot.agent.tools.mcp:connect_mcp_servers:162 - MCP: registered tool 'mcp_lms_labs' from server 'lms'
nanobot-1  | 2026-03-27 10:59:30.450 | DEBUG | nanobot.agent.tools.mcp:connect_mcp_servers:162 - MCP: registered tool 'mcp_lms_lms_learners' from server 'lms'
nanobot-1  | 2026-03-27 10:59:30.450 | DEBUG | nanobot.agent.tools.mcp:connect_mcp_servers:162 - MCP: registered tool 'mcp_lms_lms_pass_rates' from server 'lms'
nanobot-1  | 2026-03-27 10:59:30.450 | INFO  | nanobot.agent.tools.mcp:connect_mcp_servers:182 - MCP server 'lms': connected, 9 tools registered
nanobot-1  | 2026-03-27 10:59:30.450 | INFO  | nanobot.agent.loop:run:260 - Agent loop started
```

The gateway started successfully with all 9 LMS MCP tools registered. The "No channels enabled" warning is expected - the WebSocket channel will be added in Task 2B.

---

## Task 2B — Web client

### Test Results

1. **Flutter web app at `/flutter`**: ✅ Serving correctly
   - HTML page loads with Flutter bootstrap
   - `main.dart.js` is present and loads

2. **WebSocket endpoint at `/ws/chat`**: ✅ Working
   - Connection accepted with correct `access_key`
   - Agent responds with real LMS data

### Sample WebSocket Response

```json
{
  "type": "text",
  "content": "Here are the available labs:\n\n- **lab-01**: Introduction to Python\n- **lab-02**: Data Structures\n- **lab-03**: Algorithms\n\nWhich lab would you like to explore?",
  "format": "markdown"
}
```

### Files Modified

- `docker-compose.yml`: Enabled `client-web-flutter` service and Caddy dependencies
- `caddy/Caddyfile`: Uncommented `/flutter*` route
- `nanobot/config.json`: Added webchat channel configuration
- `nanobot/Dockerfile`: Added webchat channel installation
- `nanobot/pyproject.toml`: Added webchat dependency

---

## Task 3A — Structured logging

### Happy-Path Log Excerpt

When PostgreSQL is running, the backend logs show successful request flow:

```
2026-03-27 11:31:19,576 INFO [app.main] - request_started [trace_id=c3882b8e...]
2026-03-27 11:31:19,623 INFO [app.auth] - auth_success [trace_id=c3882b8e...]
2026-03-27 11:31:19,624 INFO [app.db.items] - db_query [trace_id=c3882b8e...]
2026-03-27 11:31:19,630 INFO [app.main] - request_completed [status=200] [trace_id=c3882b8e...]
```

Each log entry includes:
- `trace_id` and `span_id` for distributed tracing correlation
- `resource.service.name=Learning Management Service`
- `trace_sampled=True` indicating the trace was sampled

### Error-Path Log Excerpt (PostgreSQL Stopped)

When PostgreSQL is stopped, the logs show the failure:

```
2026-03-27 11:32:05,296 ERROR [app.db.items] - db_query [trace_id=38869cd2...]
2026-03-27 11:32:05,407 INFO [app.main] - request_completed [status=404]
```

The error log includes the exception details showing database connection failure.

### VictoriaLogs Query

Querying VictoriaLogs at `http://localhost:42002/utils/victorialogs`:

**LogsQL Query:** `*` (all logs)

**Sample Result:**
```json
{
  "_msg": "db_query",
  "_stream": "{service.name=\"Learning Management Service\"...}",
  "_time": "2026-03-27T11:32:13.743498752Z",
  "error": "[Errno -2] Name or service not known",
  "event": "db_query",
  "severity": "ERROR",
  "trace_id": "7e2ea238b0d2f16c00f911c2f5dd575c",
  "span_id": "75185bc8c6af465c"
}
```

VictoriaLogs successfully captures structured logs with:
- Full JSON structure with all fields
- Error messages preserved
- Trace/span IDs for correlation with VictoriaTraces

---

## Task 3B — Traces

### VictoriaTraces UI

Accessed at `http://localhost:42002/utils/victoriatraces` (or directly at `http://localhost:42011/select/vmui`)

### Trace Data Verification

VictoriaTraces is receiving trace data from the backend via OpenTelemetry:

**Metrics confirmation:**
```
vt_bytes_ingested_total{type="opentelemetry_traces_otlphttp_protobuf"} 147477
```

This shows 147KB+ of trace data has been ingested via OTLP HTTP protobuf format.

### Trace Structure (from logs)

From the structured logs, we can see trace correlation IDs:
- `trace_id`: e.g., `7e2ea238b0d2f16c00f911c2f5dd575c`
- `span_id`: e.g., `75185bc8c6af465c`
- `trace_sampled`: `true`

These IDs correlate logs in VictoriaLogs with spans in VictoriaTraces, enabling full distributed tracing.

### Healthy vs Error Traces

**Healthy trace flow:**
1. `request_started` span (app.main)
2. `auth_success` span (app.auth)
3. `db_query` span (app.db.items) - success
4. `request_completed` span (app.main) - status 200

**Error trace flow (PostgreSQL stopped):**
1. `request_started` span
2. `auth_success` span
3. `db_query` span - **ERROR**: `[Errno -2] Name or service not known`
4. `request_completed` span - status 404

The trace IDs remain consistent across both healthy and error scenarios, allowing correlation between logs and traces.

---

## Task 3C — Observability MCP tools

<!-- Paste agent responses to "any errors in the last hour?" under normal and failure conditions -->

## Task 4A — Multi-step investigation

<!-- Paste the agent's response to "What went wrong?" showing chained log + trace investigation -->

## Task 4B — Proactive health check

<!-- Screenshot or transcript of the proactive health report that appears in the Flutter chat -->

## Task 4C — Bug fix and recovery

<!-- 1. Root cause identified
     2. Code fix (diff or description)
     3. Post-fix response to "What went wrong?" showing the real underlying failure
     4. Healthy follow-up report or transcript after recovery -->
