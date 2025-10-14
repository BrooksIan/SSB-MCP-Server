#!/bin/bash

# SSB MCP Server wrapper script
# This script ensures the proper environment is set up for the MCP server

# Set the working directory
cd /Users/ibrooks/Documents/GitHub/SSB-MCP-Server

# Set environment variables (use values from Claude Desktop config if available)
export KNOX_GATEWAY_URL="${KNOX_GATEWAY_URL:-https://irb-ssb-test-manager0.cgsi-dem.prep-j1tk.a3.cloudera.site:443}"

# Read JWT token from Claude Desktop config if not set
if [ -z "$KNOX_TOKEN" ] || [ "$KNOX_TOKEN" = "your-jwt-token-here" ]; then
    # Try to read from claude_desktop_config.json
    if [ -f "claude_desktop_config.json" ]; then
        KNOX_TOKEN=$(python3 -c "import json; f=open('claude_desktop_config.json'); c=json.load(f); print(c['mcpServers']['ssb-mcp-server']['env']['KNOX_TOKEN']); f.close()" 2>/dev/null || echo "")
    fi
fi

export KNOX_TOKEN="${KNOX_TOKEN:-your-jwt-token-here}"
export SSB_API_BASE="${SSB_API_BASE:-}"
export SSB_USER="${SSB_USER:-}"
export SSB_PASSWORD="${SSB_PASSWORD:-}"
export SSB_READONLY="${SSB_READONLY:-false}"
export MCP_TRANSPORT="${MCP_TRANSPORT:-stdio}"
export MCP_HOST="${MCP_HOST:-127.0.0.1}"
export MCP_PORT="${MCP_PORT:-3030}"
export KNOX_VERIFY_SSL="${KNOX_VERIFY_SSL:-true}"
export HTTP_TIMEOUT_SECONDS="${HTTP_TIMEOUT_SECONDS:-60}"
export HTTP_MAX_RETRIES="${HTTP_MAX_RETRIES:-3}"
export HTTP_RATE_LIMIT_RPS="${HTTP_RATE_LIMIT_RPS:-5}"

# Legacy variables for backward compatibility
export READONLY="${SSB_READONLY}"
export TIMEOUT_SECONDS="${HTTP_TIMEOUT_SECONDS}"
export PROXY_CONTEXT_PATH=""

export PYTHONPATH="/Users/ibrooks/Documents/GitHub/SSB-MCP-Server/src"

# Debug: Print environment variables (mask sensitive token)
echo "KNOX_GATEWAY_URL: $KNOX_GATEWAY_URL"
if [ -n "$KNOX_TOKEN" ] && [ "$KNOX_TOKEN" != "your-jwt-token-here" ]; then
    echo "KNOX_TOKEN: ${KNOX_TOKEN:0:20}..."
else
    echo "KNOX_TOKEN: Not set or using placeholder"
fi
echo "SSB_READONLY: $SSB_READONLY"

# Activate the virtual environment and run the MCP server
source /Users/ibrooks/Documents/GitHub/SSB-MCP-Server/.venv/bin/activate
exec python -m ssb_mcp_server.server
