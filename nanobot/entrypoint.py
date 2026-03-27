"""Entrypoint for nanobot gateway Docker container.

Resolves environment variables into config at runtime, then launches nanobot gateway.
"""

import json
import os
import sys
from pathlib import Path


def main():
    config_path = Path("/app/nanobot/config.json")
    workspace_path = Path("/app/nanobot/workspace")
    resolved_config_path = Path("/tmp/nanobot-config-resolved.json")

    # Load config
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    # Resolve LLM provider API key from env var
    api_key = os.environ.get("LLM_API_KEY", "")
    if api_key:
        config["providers"]["custom"]["api_key"] = api_key

    # Resolve LLM API base URL
    api_base = os.environ.get("LLM_API_BASE_URL", "")
    if api_base:
        config["providers"]["custom"]["api_base"] = api_base

    # Resolve default model
    model = os.environ.get("LLM_API_MODEL", "")
    if model:
        config["agents"]["defaults"]["model"] = model

    # Resolve gateway host/port
    gateway_host = os.environ.get("NANOBOT_GATEWAY_CONTAINER_ADDRESS", "0.0.0.0")
    gateway_port = os.environ.get("NANOBOT_GATEWAY_CONTAINER_PORT", "18790")
    config["gateway"]["host"] = gateway_host
    config["gateway"]["port"] = int(gateway_port)

    # Resolve webchat host/port
    webchat_host = os.environ.get("NANOBOT_WEBCHAT_CONTAINER_ADDRESS", "0.0.0.0")
    webchat_port = os.environ.get("NANOBOT_WEBCHAT_CONTAINER_PORT", "8765")
    if "webchat" in config.get("channels", {}):
        config["channels"]["webchat"]["host"] = webchat_host
        config["channels"]["webchat"]["port"] = int(webchat_port)

    # Resolve MCP server env vars (backend URL and API key)
    if "mcp_servers" in config.get("tools", {}):
        for server_name, server_cfg in config["tools"]["mcp_servers"].items():
            backend_url = os.environ.get("NANOBOT_LMS_BACKEND_URL", "")
            if backend_url and "env" in server_cfg:
                server_cfg["env"]["NANOBOT_LMS_BACKEND_URL"] = backend_url

            api_key = os.environ.get("NANOBOT_LMS_API_KEY", "")
            if api_key and "env" in server_cfg:
                server_cfg["env"]["NANOBOT_LMS_API_KEY"] = api_key

    # Write resolved config
    with open(resolved_config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

    # Launch nanobot gateway
    os.execvp("nanobot", ["nanobot", "gateway", "--config", str(resolved_config_path), "--workspace", str(workspace_path)])


if __name__ == "__main__":
    main()
