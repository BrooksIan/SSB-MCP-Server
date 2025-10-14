#!/usr/bin/env python3
"""
Simple test to verify JWT token reading from config.
"""

import json

def test_token_reading():
    """Test reading JWT token from config file."""
    
    try:
        with open('claude_desktop_config.json', 'r') as f:
            config = json.load(f)
        
        jwt_token = config['mcpServers']['ssb-mcp-server']['env']['KNOX_TOKEN']
        knox_url = config['mcpServers']['ssb-mcp-server']['env']['KNOX_GATEWAY_URL']
        
        print("✅ Config file read successfully")
        print(f"Knox URL: {knox_url}")
        print(f"JWT Token: {jwt_token[:50]}...")
        print(f"Token length: {len(jwt_token)} characters")
        
        if jwt_token and jwt_token != "your-jwt-token-here" and len(jwt_token) > 100:
            print("✅ JWT token appears to be valid")
            return True
        else:
            print("❌ JWT token appears to be invalid or placeholder")
            return False
            
    except Exception as e:
        print(f"❌ Error reading config: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Simple JWT Token Test")
    print("=" * 30)
    
    success = test_token_reading()
    
    if success:
        print("\n🎉 JWT token is properly configured!")
    else:
        print("\n❌ JWT token configuration has issues.")
    
    exit(0 if success else 1)
