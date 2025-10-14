#!/bin/bash

# SSB MCP Server wrapper script
# This script ensures the proper environment is set up for the MCP server

# Set the working directory
cd /Users/ibrooks/Documents/GitHub/SSB-MCP-Server

# Set environment variables (use values from Claude Desktop config if available)
export KNOX_GATEWAY_URL="${KNOX_GATEWAY_URL:-https://irb-ssb-test-manager0.cgsi-dem.prep-j1tk.a3.cloudera.site:443}"

# Set JWT token for cloud SSB
export KNOX_TOKEN="eyJqa3UiOiJodHRwczovL2lyYi1zc2ItdGVzdC1tYW5hZ2VyMC5jZ3NpLWRlbS5wcmVwLWoxdGsuYTMuY2xvdWRlcmEuc2l0ZS9pcmItc3NiLXRlc3QvaG9tZXBhZ2Uva25veHRva2VuL2FwaS92Mi9qd2tzLmpzb24iLCJraWQiOiJ5VTJhOTRvOUtNVXZhalZtQmlhb1o1ajVjVVY2OTA4a09HbmdpbUdOREZNIiwidHlwIjoiSldUIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJpYnJvb2tzIiwiYXVkIjoiY2RwLXByb3h5LXRva2VuIiwiamt1IjoiaHR0cHM6Ly9pcmItc3NiLXRlc3QtbWFuYWdlcjAuY2dzaS1kZW0ucHJlcC1qMXRrLmEzLmNsb3VkZXJhLnNpdGUvaXJiLXNzYi10ZXN0L2hvbWVwYWdlL2tub3h0b2tlbi9hcGkvdjIvandrcy5qc29uIiwia2lkIjoieVUyYTk0bzlLTVV2YWpWbUJpYW9aNWo1Y1VWNjkwOGtPR25naW1HTkRGTSIsImlzcyI6IktOT1hTU08iLCJleHAiOjE3NjA1NTAxMTQsIm1hbmFnZWQudG9rZW4iOiJ0cnVlIiwia25veC5pZCI6ImM1N2UzMGJkLWFhMDUtNDNjMS05M2EwLTY4OWVhODMyNmFjZiJ9.Sie9BIK_hF2b0TT0Tujyd9ISlfe6nIQNC4IYRb9j033SSNZ6Y_TmEL_YYIOjjNnOjXGyzsAMX51AGaB1io9lSo_WE_MJUhTgW_PHkMPD8gVjKSXVxM5lHrsEepjOtmJWvYoUY9Ab47r4Qx4HCjau4_zVE-r6m9HQI2RErO0BXYhjUM88whODtNDr1ZYqhv6gxhREovMSxz3Ju2mlUhzBG-Ojt5DDpKAjCl5QjwF91Q8oMTshyC04PzBLarYC0bcuxWznxpPxlGVvIJxeeyEYms53rjICc9r8RocRszn4HnB0hAY47XyDQRjLv8UbctJTd0oImMMEKv0F3kucSHSSUw"
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
