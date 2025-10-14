#!/usr/bin/env python3
"""
Quick script to check JWT token expiration.
"""

import json
import base64
from datetime import datetime

def check_token_expiry():
    """Check if JWT token is expired."""
    
    try:
        # Read JWT token from config
        with open('claude_desktop_config.json', 'r') as f:
            config = json.load(f)
        jwt_token = config['mcpServers']['ssb-mcp-server']['env']['KNOX_TOKEN']
    except Exception as e:
        print(f"❌ Error reading config: {e}")
        return False
    
    try:
        # Decode JWT payload
        parts = jwt_token.split('.')
        payload = json.loads(base64.urlsafe_b64decode(parts[1] + '=='))
        
        if 'exp' in payload:
            exp_timestamp = payload['exp']
            exp_date = datetime.fromtimestamp(exp_timestamp)
            current_date = datetime.now()
            
            print(f"JWT Token Expiration: {exp_date}")
            print(f"Current Time: {current_date}")
            
            if current_date > exp_date:
                print("❌ JWT TOKEN IS EXPIRED!")
                print("You need to get a new token from CDP/Cloudera Manager.")
                return False
            else:
                time_left = exp_date - current_date
                print(f"✅ JWT token is valid for {time_left}")
                return True
        else:
            print("⚠️  No expiration found in token")
            return True
            
    except Exception as e:
        print(f"❌ Error decoding JWT token: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Checking JWT Token Expiration")
    print("=" * 40)
    
    is_valid = check_token_expiry()
    
    if not is_valid:
        print("\n💡 To get a new token:")
        print("1. Go to CDP/Cloudera Manager")
        print("2. Navigate to SSB service")
        print("3. Get a new JWT token")
        print("4. Update claude_desktop_config.json")
    
    exit(0 if is_valid else 1)
