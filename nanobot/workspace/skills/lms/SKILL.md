---
nanobot:
  always: true
  description: "Use LMS MCP tools to answer questions about labs, learners, and analytics"
---

# LMS Analytics Skill

**Available:** true

## Purpose

This skill teaches you how to use the LMS MCP tools to answer questions about labs, learners, and analytics data.

## Available Tools

You have access to these LMS tools via MCP:

| Tool | Description | Parameters |
|------|-------------|------------|
| `lms_health` | Check if the LMS backend is healthy and get item count | None |
| `lms_labs` | List all labs available in the LMS | None |
| `lms_learners` | List all registered learners | None |
| `lms_pass_rates` | Get pass rates (avg score, attempt count per task) for a lab | `lab` (required): Lab identifier like "lab-01" |
| `lms_timeline` | Get submission timeline (date + count) for a lab | `lab` (required) |
| `lms_groups` | Get group performance (avg score + student count) for a lab | `lab` (required) |
| `lms_top_learners` | Get top learners by average score for a lab | `lab` (required), `limit` (optional, default 5) |
| `lms_completion_rate` | Get completion rate (passed/total) for a lab | `lab` (required) |
| `lms_sync_pipeline` | Trigger the LMS sync pipeline | None |

## How to Use

### When the user asks about available labs

Call `lms_labs` first to get the list of labs. Then you can offer to show more details about specific labs.

### When the user asks about scores or pass rates WITHOUT specifying a lab

**Important:** If the user says "show me the scores" or "what are the pass rates" without specifying which lab:

1. First call `lms_labs` to get available labs
2. Then respond with: "Which lab would you like to see? Available labs: lab-01, lab-02, lab-03"
3. OR list the labs with brief descriptions and ask the user to choose

**Do NOT** guess the lab or pick one arbitrarily.

### When the user asks about top learners

Call `lms_top_learners` with the specified lab. If no limit is given, use the default of 5.

### When the user asks about completion or pass rates

Call `lms_completion_rate` or `lms_pass_rates` with the lab parameter.

### Formatting results

- Format numeric results nicely: show percentages as "75%" not "0.75"
- Round decimal scores to 1-2 decimal places
- Present data in tables when appropriate
- Keep responses concise - summarize the key findings, don't dump raw JSON

## Example Interactions

### Example 1: User asks "What labs are available?"

```
You: Call lms_labs → get ["lab-01", "lab-02", "lab-03"]
Response: "Here are the available labs:
- lab-01: Introduction to Python
- lab-02: Data Structures  
- lab-03: Algorithms

Which lab would you like to explore?"
```

### Example 2: User asks "Show me the scores" (no lab specified)

```
You: Call lms_labs first to see what's available
Response: "I can show scores, but which lab would you like to see? Available options:
- lab-01: Introduction to Python
- lab-02: Data Structures
- lab-03: Algorithms"
```

### Example 3: User asks "What's the pass rate for lab-01?"

```
You: Call lms_pass_rates with lab="lab-01"
Response: "Here are the pass rates for lab-01:
| Task | Avg Score | Avg Attempts |
|------|-----------|--------------|
| task-01 | 85% | 2.3 |
| task-02 | 72% | 3.1 |"
```

## Limits

- You can only query data that exists in the LMS backend
- If a tool returns an error, explain what went wrong clearly
- If the backend is unavailable, say so honestly rather than hallucinating data
