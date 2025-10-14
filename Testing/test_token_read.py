#!/usr/bin/env python3
"""
Test script to verify JWT token is being read correctly from config.
"""

import json
import os

def test_token_read():
    """Test reading JWT token from config file."""
    
    print("🔍 Testing JWT Token Reading")
    print("=" * 40)
    
    try:
        # Read config file
        with open('claude_desktop_config.json', 'r') as f:
            config = json.load(f)
        
        # Extract JWT token
        jwt_token = config['mcpServers']['ssb-mcp-server']['env']['KNOX_TOKEN']
        knox_url = config['mcpServers']['ssb-mcp-server']['env']['KNOX_GATEWAY_URL']
        
        print(f"✅ Config file read successfully")
        print(f"Knox URL: {knox_url}")
        print(f"JWT Token: {jwt_token[:50]}...")
        print(f"Token length: {len(jwt_token)} characters")
        
        # Check if token looks valid
        if jwt_token and jwt_token != "your-jwt-token-here" and len(jwt_token) > 100:
            print("✅ JWT token appears to be valid")
            return True
        else:
            print("❌ JWT token appears to be invalid or placeholder")
            return False
            
    except Exception as e:
        print(f"❌ Error reading config: {e}")
        return False

def test_environment_variables():
    """Test environment variable setup."""
    
    print("\n🌍 Testing Environment Variables")
    print("=" * 40)
    
    # Set up environment like the shell script would
    os.environ['KNOX_GATEWAY_URL'] = 'https://irb-ssb-test-manager0.cgsi-dem.prep-j1tk.a3.cloudera.site:443'
    
    # Read token from config
    try:
        with open('claude_desktop_config.json', 'r') as f:
            config = json.load(f)
        jwt_token = config['mcpServers']['ssb-mcp-server']['env']['KNOX_TOKEN']
        os.environ['KNOX_TOKEN'] = jwt_token
    except Exception as e:
        print(f"❌ Error setting up environment: {e}")
        return False
    
    print(f"KNOX_GATEWAY_URL: {os.environ.get('KNOX_GATEWAY_URL')}")
    print(f"KNOX_TOKEN: {os.environ.get('KNOX_TOKEN', 'Not set')[:50]}...")
    
    return True

if __name__ == "__main__":
    success1 = test_token_read()
    success2 = test_environment_variables()
    
    if success1 and success2:
        print("\n🎉 JWT token configuration is working correctly!")
    else:
        print("\n❌ JWT token configuration has issues.")
    
    exit(0 if (success1 and success2) else 1)
