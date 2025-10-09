#!/bin/bash

# SSB MCP Server wrapper script
# This script ensures the proper environment is set up for the MCP server

# Set the working directory
cd /Users/ibrooks/Documents/GitHub/SSB-MCP-Server

# Set environment variables
export SSB_API_BASE="http://localhost:18121"
export READONLY="false"
export TIMEOUT_SECONDS="30"
export PROXY_CONTEXT_PATH=""

# SSB Authentication (using basic auth)
export SSB_USER="admin"
export SSB_PASSWORD="admin"

export PYTHONPATH="/Users/ibrooks/Documents/GitHub/SSB-MCP-Server/src"

# Activate the virtual environment and run the MCP server
exec /Users/ibrooks/Documents/GitHub/SSB-MCP-Server/.venv/bin/python -m ssb_mcp_server.server
