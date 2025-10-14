#!/usr/bin/env python3
"""
Test JWT token connection using the configured token from claude_desktop_config.json
"""

import os
import sys
import json
import requests

def test_jwt_connection():
    """Test JWT token connection using the configured token."""
    
    # Read the JWT token from config
    try:
        with open('claude_desktop_config.json', 'r') as f:
            config = json.load(f)
        
        jwt_token = config['mcpServers']['ssb-mcp-server']['env']['KNOX_TOKEN']
        knox_gateway_url = config['mcpServers']['ssb-mcp-server']['env']['KNOX_GATEWAY_URL']
        
        print("🔐 Testing JWT Token Connection")
        print("=" * 50)
        print(f"Knox Gateway: {knox_gateway_url}")
        print(f"JWT Token: {jwt_token[:50]}...")
        
    except Exception as e:
        print(f"❌ Error reading config: {e}")
        return False
    
    try:
        # Test SSB API endpoint through Knox
        ssb_api_url = f"{knox_gateway_url}/irb-ssb-test/cdp-proxy-token/ssb-mve-api"
        info_url = f"{ssb_api_url}/api/v1/info"
        
        print(f"\n📡 Testing SSB API endpoint...")
        print(f"SSB API URL: {ssb_api_url}")
        print(f"Info URL: {info_url}")
        
        # JWT token authentication
        headers = {
            'Authorization': f'Bearer {jwt_token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(info_url, headers=headers, timeout=30, verify=True)
        
        if response.status_code == 200:
            print("✅ SSB API accessible with JWT token!")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"❌ SSB API error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.SSLError as e:
        print(f"❌ SSL Error: {e}")
        return False
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Connection Error: {e}")
        return False
    except requests.exceptions.Timeout as e:
        print(f"❌ Timeout Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False

def test_mcp_server():
    """Test MCP server with the configured JWT token."""
    
    print("\n🧪 Testing MCP Server with JWT token...")
    
    try:
        # Read config and set environment
        with open('claude_desktop_config.json', 'r') as f:
            config = json.load(f)
        
        env_vars = config['mcpServers']['ssb-mcp-server']['env']
        os.environ.update(env_vars)
        
        # Import and test the MCP server
        sys.path.insert(0, '/Users/ibrooks/Documents/GitHub/SSB-MCP-Server/src')
        from ssb_mcp_server.config import ServerConfig
        from ssb_mcp_server.client import SSBClient
        
        print("✅ MCP server modules imported successfully")
        
        # Test configuration
        config_obj = ServerConfig()
        print(f"✅ Configuration loaded: {config_obj.knox_gateway_url}")
        
        # Test client creation
        client = SSBClient(config_obj)
        print("✅ SSB client created successfully")
        
        # Test SSB info
        info = client.get_ssb_info()
        print(f"✅ SSB Info: {info}")
        
        return True
        
    except Exception as e:
        print(f"❌ MCP Server Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 JWT Token Connection Test")
    print("=" * 50)
    
    # Test 1: Direct API connection
    success1 = test_jwt_connection()
    
    if success1:
        # Test 2: MCP server integration
        success2 = test_mcp_server()
        
        if success2:
            print("\n🎉 All tests passed! JWT token is working correctly.")
            print("You can now restart Claude Desktop to use the MCP server.")
        else:
            print("\n⚠️  API connection works, but MCP server needs debugging.")
    else:
        print("\n❌ JWT token connection failed. Check the token and network access.")
    
    sys.exit(0 if success1 else 1)
