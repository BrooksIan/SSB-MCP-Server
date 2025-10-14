#!/usr/bin/env python3
"""
Configuration loader for SSB MCP Server.
Loads configuration from config/cloud_ssb_config.json
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

class ConfigLoader:
    """Loads and manages configuration for SSB MCP Server."""
    
    def __init__(self, config_file: str = "config/cloud_ssb_config.json"):
        """Initialize config loader with config file path."""
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        try:
            config_path = Path(self.config_file)
            if not config_path.exists():
                raise FileNotFoundError(f"Config file not found: {self.config_file}")
            
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            return {}
    
    def get_cloud_ssb_config(self) -> Dict[str, Any]:
        """Get cloud SSB configuration."""
        return self.config.get('cloud_ssb', {})
    
    def get_local_ssb_config(self) -> Dict[str, Any]:
        """Get local SSB configuration."""
        return self.config.get('local_ssb', {})
    
    def get_mcp_server_config(self) -> Dict[str, Any]:
        """Get MCP server configuration."""
        return self.config.get('mcp_server', {})
    
    def get_knox_gateway_url(self) -> Optional[str]:
        """Get Knox Gateway URL."""
        return self.get_cloud_ssb_config().get('knox_gateway_url')
    
    def get_jwt_token(self) -> Optional[str]:
        """Get JWT token."""
        return self.get_cloud_ssb_config().get('jwt_token')
    
    def get_ssb_api_base(self, use_cloud: bool = True) -> Optional[str]:
        """Get SSB API base URL."""
        if use_cloud:
            return self.get_cloud_ssb_config().get('ssb_api_base')
        else:
            return self.get_local_ssb_config().get('ssb_api_base')
    
    def get_environment_variables(self, use_cloud: bool = True) -> Dict[str, str]:
        """Get environment variables for the specified configuration."""
        if use_cloud:
            config = self.get_cloud_ssb_config()
            return {
                'KNOX_GATEWAY_URL': config.get('knox_gateway_url', ''),
                'KNOX_TOKEN': config.get('jwt_token', ''),
                'SSB_API_BASE': config.get('ssb_api_base', ''),
                'SSB_READONLY': str(config.get('ssb_readonly', False)).lower(),
                'KNOX_VERIFY_SSL': str(config.get('knox_verify_ssl', True)).lower(),
                'HTTP_TIMEOUT_SECONDS': str(config.get('http_timeout_seconds', 60)),
                'HTTP_MAX_RETRIES': str(config.get('http_max_retries', 3)),
                'HTTP_RATE_LIMIT_RPS': str(config.get('http_rate_limit_rps', 5))
            }
        else:
            config = self.get_local_ssb_config()
            return {
                'SSB_API_BASE': config.get('ssb_api_base', ''),
                'SSB_USER': config.get('ssb_user', ''),
                'SSB_PASSWORD': config.get('ssb_password', ''),
                'SSB_READONLY': str(config.get('ssb_readonly', False)).lower(),
                'HTTP_TIMEOUT_SECONDS': str(config.get('http_timeout_seconds', 30))
            }
    
    def update_jwt_token(self, new_token: str) -> bool:
        """Update JWT token in config file."""
        try:
            if 'cloud_ssb' not in self.config:
                self.config['cloud_ssb'] = {}
            
            self.config['cloud_ssb']['jwt_token'] = new_token
            
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error updating JWT token: {e}")
            return False
    
    def update_knox_gateway_url(self, new_url: str) -> bool:
        """Update Knox Gateway URL in config file."""
        try:
            if 'cloud_ssb' not in self.config:
                self.config['cloud_ssb'] = {}
            
            self.config['cloud_ssb']['knox_gateway_url'] = new_url
            # Also update the SSB API base URL
            self.config['cloud_ssb']['ssb_api_base'] = f"{new_url}/irb-ssb-test/cdp-proxy-token/ssb-sse-api/api/v1"
            
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error updating Knox Gateway URL: {e}")
            return False
    
    def print_config(self, use_cloud: bool = True):
        """Print current configuration."""
        print(f"🔧 SSB MCP Server Configuration ({'Cloud' if use_cloud else 'Local'})")
        print("=" * 60)
        
        if use_cloud:
            config = self.get_cloud_ssb_config()
            print(f"Knox Gateway URL: {config.get('knox_gateway_url', 'Not set')}")
            print(f"SSB API Base: {config.get('ssb_api_base', 'Not set')}")
            print(f"JWT Token: {config.get('jwt_token', 'Not set')[:50]}..." if config.get('jwt_token') else "JWT Token: Not set")
            print(f"SSB Readonly: {config.get('ssb_readonly', False)}")
            print(f"Knox Verify SSL: {config.get('knox_verify_ssl', True)}")
            print(f"HTTP Timeout: {config.get('http_timeout_seconds', 60)}s")
        else:
            config = self.get_local_ssb_config()
            print(f"SSB API Base: {config.get('ssb_api_base', 'Not set')}")
            print(f"SSB User: {config.get('ssb_user', 'Not set')}")
            print(f"SSB Password: {'*' * len(config.get('ssb_password', '')) if config.get('ssb_password') else 'Not set'}")
            print(f"SSB Readonly: {config.get('ssb_readonly', False)}")
            print(f"HTTP Timeout: {config.get('http_timeout_seconds', 30)}s")

def main():
    """Main function for testing config loader."""
    loader = ConfigLoader()
    
    # Print cloud configuration
    loader.print_config(use_cloud=True)
    
    print("\n" + "=" * 60)
    
    # Print local configuration
    loader.print_config(use_cloud=False)
    
    print("\n" + "=" * 60)
    
    # Print environment variables
    print("Environment Variables (Cloud):")
    env_vars = loader.get_environment_variables(use_cloud=True)
    for key, value in env_vars.items():
        if 'TOKEN' in key or 'PASSWORD' in key:
            print(f"  {key}: {value[:20]}..." if value else f"  {key}: Not set")
        else:
            print(f"  {key}: {value}")

if __name__ == "__main__":
    main()
