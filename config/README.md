# Configuration Setup

This directory contains configuration files for the SSB MCP Server.

## Files

- `cloud_ssb_config.json.example` - Template configuration file with placeholder values
- `cloud_ssb_config.json` - Your actual configuration file (not tracked in git)

## Setup Instructions

1. Copy the example file to create your actual configuration:
   ```bash
   cp config/cloud_ssb_config.json.example config/cloud_ssb_config.json
   ```

2. Edit `config/cloud_ssb_config.json` and replace the placeholder values with your actual configuration:
   - `knox_gateway_url`: Your Knox Gateway URL
   - `jwt_token`: Your JWT authentication token
   - `pythonpath`: Path to your SSB-MCP-Server src directory

## Security Note

The `cloud_ssb_config.json` file contains sensitive information (JWT tokens, URLs) and is excluded from git tracking. Always use the `.example` file as a template and never commit your actual configuration file.

## Configuration Sections

### Cloud SSB Configuration
- `knox_gateway_url`: The Knox Gateway URL for your SSB instance
- `ssb_api_base`: The base API URL for SSB services
- `jwt_token`: Your JWT authentication token
- `ssb_readonly`: Whether to run in read-only mode
- `knox_verify_ssl`: Whether to verify SSL certificates
- `http_timeout_seconds`: HTTP request timeout
- `http_max_retries`: Maximum number of retry attempts
- `http_rate_limit_rps`: Rate limit for requests per second

### Local SSB Configuration
- `ssb_api_base`: Local SSB API URL
- `ssb_user`: Username for local SSB
- `ssb_password`: Password for local SSB
- `ssb_readonly`: Whether to run in read-only mode
- `http_timeout_seconds`: HTTP request timeout

### MCP Server Configuration
- `transport`: Transport method (stdio)
- `host`: Server host
- `port`: Server port
- `pythonpath`: Path to the Python source code
