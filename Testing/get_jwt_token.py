#!/usr/bin/env python3
"""
Helper script to obtain JWT token for CDP/SSB authentication.
This script helps you get a JWT token for use with the MCP server.
"""

import requests
import json
import sys
from urllib.parse import urljoin

def get_jwt_token_from_username_password():
    """Get JWT token using username/password authentication."""
    
    knox_gateway_url = "https://irb-ssb-test-manager0.cgsi-dem.prep-j1tk.a3.cloudera.site:443"
    
    print("🔐 Getting JWT Token for CDP/SSB Authentication")
    print("=" * 50)
    print(f"Knox Gateway: {knox_gateway_url}")
    
    username = input("Enter your CDP username: ")
    password = input("Enter your CDP password: ")
    
    try:
        # Try to get token from Knox Gateway
        token_url = f"{knox_gateway_url}/gateway/irb-ssb-test/cdp-proxy-token/ssb-mve-api/api/v1/token"
        
        print(f"\n📡 Requesting token from: {token_url}")
        
        # Basic authentication to get token
        auth = (username, password)
        response = requests.post(
            token_url,
            auth=auth,
            headers={'Content-Type': 'application/json'},
            timeout=30,
            verify=True
        )
        
        if response.status_code == 200:
            token_data = response.json()
            if 'access_token' in token_data:
                jwt_token = token_data['access_token']
                print(f"✅ JWT Token obtained successfully!")
                print(f"Token: {jwt_token[:50]}...")
                return jwt_token
            else:
                print(f"❌ No access_token in response: {token_data}")
                return None
        else:
            print(f"❌ Token request failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except requests.exceptions.SSLError as e:
        print(f"❌ SSL Error: {e}")
        print("Try with KNOX_VERIFY_SSL=false for testing")
        return None
    except Exception as e:
        print(f"❌ Error getting token: {e}")
        return None

def test_jwt_token(jwt_token):
    """Test if the JWT token works with SSB API."""
    
    if not jwt_token:
        print("❌ No token to test")
        return False
    
    knox_gateway_url = "https://irb-ssb-test-manager0.cgsi-dem.prep-j1tk.a3.cloudera.site:443"
    ssb_api_url = f"{knox_gateway_url}/irb-ssb-test/cdp-proxy-token/ssb-mve-api"
    
    try:
        print(f"\n🧪 Testing JWT token with SSB API...")
        
        headers = {
            'Authorization': f'Bearer {jwt_token}',
            'Content-Type': 'application/json'
        }
        
        # Test with SSB info endpoint
        info_url = f"{ssb_api_url}/api/v1/info"
        response = requests.get(info_url, headers=headers, timeout=30, verify=True)
        
        if response.status_code == 200:
            print("✅ JWT token works with SSB API!")
            print(f"SSB Info: {response.json()}")
            return True
        else:
            print(f"❌ JWT token test failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing token: {e}")
        return False

def save_token_to_config(jwt_token):
    """Save the JWT token to the Claude Desktop config."""
    
    if not jwt_token:
        print("❌ No token to save")
        return False
    
    config_file = "claude_desktop_config.json"
    
    try:
        # Read current config
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        # Update the token
        if 'mcpServers' in config and 'ssb-mcp-server' in config['mcpServers']:
            config['mcpServers']['ssb-mcp-server']['env']['KNOX_TOKEN'] = jwt_token
            print(f"✅ Updated {config_file} with JWT token")
        else:
            print(f"❌ Could not find ssb-mcp-server in {config_file}")
            return False
        
        # Write back to file
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print("✅ Configuration updated successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error updating config: {e}")
        return False

def main():
    """Main function to get and configure JWT token."""
    
    print("🚀 CDP/SSB JWT Token Helper")
    print("=" * 50)
    
    # Get JWT token
    jwt_token = get_jwt_token_from_username_password()
    
    if jwt_token:
        # Test the token
        if test_jwt_token(jwt_token):
            # Save to config
            if save_token_to_config(jwt_token):
                print("\n🎉 JWT token configured successfully!")
                print("You can now restart Claude Desktop to use the MCP server.")
            else:
                print("\n⚠️  Token obtained but failed to save to config.")
        else:
            print("\n⚠️  Token obtained but doesn't work with SSB API.")
    else:
        print("\n❌ Failed to obtain JWT token.")
        print("Please check your credentials and network access.")
    
    return jwt_token is not None

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
