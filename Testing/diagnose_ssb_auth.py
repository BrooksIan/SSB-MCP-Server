#!/usr/bin/env python3
"""
Comprehensive diagnostic script for SSB authentication issues.
"""

import json
import requests
import base64
import sys
import os
from datetime import datetime

# Add parent directory to Python path to access config module
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from config.config_loader import ConfigLoader

def decode_jwt_token(jwt_token):
    """Decode JWT token to check expiration and claims."""
    
    print("🔍 Analyzing JWT Token")
    print("=" * 40)
    
    try:
        # Split JWT token (header.payload.signature)
        parts = jwt_token.split('.')
        if len(parts) != 3:
            print("❌ Invalid JWT token format")
            return False
        
        # Decode header and payload (add padding if needed)
        header = json.loads(base64.urlsafe_b64decode(parts[0] + '=='))
        payload = json.loads(base64.urlsafe_b64decode(parts[1] + '=='))
        
        print(f"Header: {json.dumps(header, indent=2)}")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        # Check expiration
        if 'exp' in payload:
            exp_timestamp = payload['exp']
            exp_date = datetime.fromtimestamp(exp_timestamp)
            current_date = datetime.now()
            
            print(f"\nToken Expiration: {exp_date}")
            print(f"Current Time: {current_date}")
            
            if current_date > exp_date:
                print("❌ JWT TOKEN IS EXPIRED!")
                return False
            else:
                print("✅ JWT token is still valid")
                return True
        else:
            print("⚠️  No expiration found in token")
            return True
            
    except Exception as e:
        print(f"❌ Error decoding JWT token: {e}")
        return False

def test_knox_gateway_endpoints():
    """Test various Knox Gateway endpoints to find the right one."""
    
    print("\n🌐 Testing Knox Gateway Endpoints")
    print("=" * 40)
    
    # Load Cloud SSB configuration
    config_loader = ConfigLoader()
    cloud_config = config_loader.get_cloud_ssb_config()
    
    knox_url = cloud_config.get('knox_gateway_url')
    jwt_token = cloud_config.get('jwt_token')
    
    # Test different possible endpoints
    base_endpoints = [
        "/irb-ssb-test/cdp-proxy-token/ssb-sse-api",
        "/irb-ssb-test/cdp-proxy-token/ssb-mve-api",
        "/irb-ssb-test/cdp-proxy/ssb-mve-api",
        "/irb-ssb-test/cdp-proxy/ssb-sse-api",
        "/irb-ssb-test/cdp-proxy-api/ssb-mve-api",
        "/irb-ssb-test/cdp-proxy-api/ssb-ssb-api/"
    ]
    
    api_endpoints = [
        "/api/v1/info",
        "/api/v1",
        "/api/v1/tables",
        "/api/v1/jobs",
        "/api/v1/data-sources",
        "/api/v2/projects",
        "/api/v2/projects/info",
        "/info",
        "/health",
        "/status"
    ]
    
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'Content-Type': 'application/json'
    }
    
    working_endpoints = []
    
    for base in base_endpoints:
        for api in api_endpoints:
            endpoint = f"{knox_url}{base}{api}"
            print(f"\nTesting: {endpoint}")
            
            try:
                response = requests.get(endpoint, headers=headers, timeout=10, verify=True)
                print(f"  Status: {response.status_code}")
                
                if response.status_code == 200:
                    print(f"  ✅ SUCCESS!")
                    print(f"  Response: {response.json()}")
                    working_endpoints.append(endpoint)
                elif response.status_code == 401:
                    print(f"  🔐 Authentication required (401)")
                elif response.status_code == 403:
                    print(f"  🚫 Forbidden (403)")
                elif response.status_code == 404:
                    print(f"  ❌ Not found (404)")
                else:
                    print(f"  ⚠️  Status {response.status_code}: {response.text[:100]}")
                    
            except Exception as e:
                print(f"  ❌ Error: {e}")
    
    if working_endpoints:
        print(f"\n🎉 Found {len(working_endpoints)} working endpoint(s):")
        for endpoint in working_endpoints:
            print(f"  - {endpoint}")
        return True
    else:
        print("\n❌ No working endpoints found")
        return False

def test_authentication_methods():
    """Test different authentication methods."""
    
    print("\n🔐 Testing Authentication Methods")
    print("=" * 40)
    
    # Load Cloud SSB configuration
    config_loader = ConfigLoader()
    cloud_config = config_loader.get_cloud_ssb_config()
    
    knox_url = cloud_config.get('knox_gateway_url')
    jwt_token = cloud_config.get('jwt_token')
    
    # Test with the most likely endpoint
    endpoint = f"{knox_url}/irb-ssb-test/cdp-proxy-token/ssb-sse-api/api/v1/info"
    
    auth_methods = [
        ("Bearer Token", {'Authorization': f'Bearer {jwt_token}'}),
        ("Token Header", {'X-Auth-Token': jwt_token}),
        ("Knox Token", {'X-Knox-Token': jwt_token}),
        ("CDP Token", {'X-CDP-Token': jwt_token}),
        ("Custom Auth", {'Authorization': f'Token {jwt_token}'}),
    ]
    
    for method_name, headers in auth_methods:
        print(f"\nTesting {method_name}:")
        try:
            response = requests.get(endpoint, headers=headers, timeout=10, verify=True)
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"  ✅ SUCCESS with {method_name}!")
                print(f"  Response: {response.json()}")
                return True
            else:
                print(f"  ❌ Failed: {response.text[:100]}")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    return False

def test_knox_gateway_info():
    """Test Knox Gateway information and capabilities."""
    
    print("\n🌐 Testing Knox Gateway Information")
    print("=" * 40)
    
    try:
        with open('claude_desktop_config.json', 'r') as f:
            config = json.load(f)
        knox_url = config['mcpServers']['ssb-mcp-server']['env']['KNOX_GATEWAY_URL']
    except Exception as e:
        print(f"❌ Error reading config: {e}")
        return False
    
    # Test basic connectivity
    try:
        response = requests.get(knox_url, timeout=10, verify=True)
        print(f"Knox Gateway Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Knox Gateway is accessible")
        else:
            print(f"❌ Knox Gateway error: {response.text[:200]}")
    except Exception as e:
        print(f"❌ Knox Gateway error: {e}")
    
    # Test Knox info endpoints
    info_endpoints = [
        f"{knox_url}/gateway/irb-ssb-test/info",
        f"{knox_url}/gateway/info",
        f"{knox_url}/irb-ssb-test/info",
        f"{knox_url}/info"
    ]
    
    for info_url in info_endpoints:
        try:
            response = requests.get(info_url, timeout=10, verify=True)
            print(f"\nInfo endpoint {info_url}:")
            print(f"  Status: {response.status_code}")
            if response.status_code == 200:
                print(f"  ✅ Response: {response.json()}")
            else:
                print(f"  ❌ Error: {response.text[:100]}")
        except Exception as e:
            print(f"  ❌ Error: {e}")

def main():
    """Main diagnostic function."""
    
    print("🚀 SSB Authentication Diagnostic Tool")
    print("=" * 50)
    
    # Use hardcoded values since config is simplified
    jwt_token = "eyJqa3UiOiJodHRwczovL2lyYi1zc2ItdGVzdC1tYW5hZ2VyMC5jZ3NpLWRlbS5wcmVwLWoxdGsuYTMuY2xvdWRlcmEuc2l0ZS9pcmItc3NiLXRlc3QvaG9tZXBhZ2Uva25veHRva2VuL2FwaS92Mi9qd2tzLmpzb24iLCJraWQiOiJ5VTJhOTRvOUtNVXZhalZtQmlhb1o1ajVjVVY2OTA4a09HbmdpbUdOREZNIiwidHlwIjoiSldUIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJpYnJvb2tzIiwiYXVkIjoiY2RwLXByb3h5LXRva2VuIiwiamt1IjoiaHR0cHM6Ly9pcmItc3NiLXRlc3QtbWFuYWdlcjAuY2dzaS1kZW0ucHJlcC1qMXRrLmEzLmNsb3VkZXJhLnNpdGUvaXJiLXNzYi10ZXN0L2hvbWVwYWdlL2tub3h0b2tlbi9hcGkvdjIvandrcy5qc29uIiwia2lkIjoieVUyYTk0bzlLTVV2YWpWbUJpYW9aNWo1Y1VWNjkwOGtPR25naW1HTkRGTSIsImlzcyI6IktOT1hTU08iLCJleHAiOjE3NjA1NTAxMTQsIm1hbmFnZWQudG9rZW4iOiJ0cnVlIiwia25veC5pZCI6ImM1N2UzMGJkLWFhMDUtNDNjMS05M2EwLTY4OWVhODMyNmFjZiJ9.Sie9BIK_hF2b0TT0Tujyd9ISlfe6nIQNC4IYRb9j033SSNZ6Y_TmEL_YYIOjjNnOjXGyzsAMX51AGaB1io9lSo_WE_MJUhTgW_PHkMPD8gVjKSXVxM5lHrsEepjOtmJWvYoUY9Ab47r4Qx4HCjau4_zVE-r6m9HQI2RErO0BXYhjUM88whODtNDr1ZYqhv6gxhREovMSxz3Ju2mlUhzBG-Ojt5DDpKAjCl5QjwF91Q8oMTshyC04PzBLarYC0bcuxWznxpPxlGVvIJxeeyEYms53rjICc9r8RocRszn4HnB0hAY47XyDQRjLv8UbctJTd0oImMMEKv0F3kucSHSSUw"
    
    print(f"JWT Token: {jwt_token[:50]}...")
    
    # Step 1: Analyze JWT token
    token_valid = decode_jwt_token(jwt_token)
    
    if not token_valid:
        print("\n❌ JWT token is expired or invalid. Please get a new token.")
        return False
    
    # Step 2: Test Knox Gateway endpoints
    endpoints_work = test_knox_gateway_endpoints()
    
    if not endpoints_work:
        # Step 3: Test different auth methods
        auth_works = test_authentication_methods()
        
        if not auth_works:
            # Step 4: Test Knox Gateway info
            test_knox_gateway_info()
    
    print("\n" + "=" * 50)
    print("Diagnostic complete. Check the results above for solutions.")
    
    return token_valid

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
