#!/usr/bin/env python3
"""
Test script for cloud SSB connection via Knox Gateway.
"""

import os
import sys
import json
import requests
from urllib.parse import urljoin

def test_cloud_ssb_connection():
    """Test connection to cloud SSB via Knox Gateway with JWT token."""
    
    # Cloud SSB configuration
    knox_gateway_url = "https://irb-ssb-test-manager0.cgsi-dem.prep-j1tk.a3.cloudera.site:443"
    jwt_token = "eyJqa3UiOiJodHRwczovL2lyYi1zc2ItdGVzdC1tYW5hZ2VyMC5jZ3NpLWRlbS5wcmVwLWoxdGsuYTMuY2xvdWRlcmEuc2l0ZS9pcmItc3NiLXRlc3QvaG9tZXBhZ2Uva25veHRva2VuL2FwaS92Mi9qd2tzLmpzb24iLCJraWQiOiJ5VTJhOTRvOUtNVXZhalZtQmlhb1o1ajVjVVY2OTA4a09HbmdpbUdOREZNIiwidHlwIjoiSldUIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJpYnJvb2tzIiwiYXVkIjoiY2RwLXByb3h5LXRva2VuIiwiamt1IjoiaHR0cHM6Ly9pcmItc3NiLXRlc3QtbWFuYWdlcjAuY2dzaS1kZW0ucHJlcC1qMXRrLmEzLmNsb3VkZXJhLnNpdGUvaXJiLXNzYi10ZXN0L2hvbWVwYWdlL2tub3h0b2tlbi9hcGkvdjIvandrcy5qc29uIiwia2lkIjoieVUyYTk0bzlLTVV2YWpWbUJpYW9aNWo1Y1VWNjkwOGtPR25naW1HTkRGTSIsImlzcyI6IktOT1hTU08iLCJleHAiOjE3NjA1NTAxMTQsIm1hbmFnZWQudG9rZW4iOiJ0cnVlIiwia25veC5pZCI6ImM1N2UzMGJkLWFhMDUtNDNjMS05M2EwLTY4OWVhODMyNmFjZiJ9.Sie9BIK_hF2b0TT0Tujyd9ISlfe6nIQNC4IYRb9j033SSNZ6Y_TmEL_YYIOjjNnOjXGyzsAMX51AGaB1io9lSo_WE_MJUhTgW_PHkMPD8gVjKSXVxM5lHrsEepjOtmJWvYoUY9Ab47r4Qx4HCjau4_zVE-r6m9HQI2RErO0BXYhjUM88whODtNDr1ZYqhv6gxhREovMSxz3Ju2mlUhzBG-Ojt5DDpKAjCl5QjwF91Q8oMTshyC04PzBLarYC0bcuxWznxpPxlGVvIJxeeyEYms53rjICc9r8RocRszn4HnB0hAY47XyDQRjLv8UbctJTd0oImMMEKv0F3kucSHSSUw"

    
    print(f"\n🌐 Testing connection to cloud SSB...")
    print(f"Knox Gateway: {knox_gateway_url}")
    print(f"JWT Token: {jwt_token[:20]}..." if len(jwt_token) > 20 else f"JWT Token: {jwt_token}")
    
    try:
        # Test Knox Gateway connectivity
        print("\n1. Testing Knox Gateway connectivity...")
        response = requests.get(knox_gateway_url, timeout=10, verify=True)
        print(f"✅ Knox Gateway accessible: {response.status_code}")
        
        # Test SSB API endpoint through Knox
        ssb_api_url = f"{knox_gateway_url}/irb-ssb-test/cdp-proxy-token/ssb-mve-api"
        print(f"\n2. Testing SSB API endpoint...")
        print(f"SSB API URL: {ssb_api_url}")
        
        # Try to access SSB info endpoint
        info_url = f"{ssb_api_url}/api/v1/info"
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
        print("Try setting KNOX_VERIFY_SSL=false for testing")
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

def test_mcp_server_with_cloud_ssb():
    """Test MCP server with cloud SSB configuration using JWT token."""
    
    print("\n🧪 Testing MCP Server with cloud SSB...")
    
    # Set environment variables
    os.environ.update({
        'KNOX_GATEWAY_URL': 'https://irb-ssb-test-manager0.cgsi-dem.prep-j1tk.a3.cloudera.site:443',
        'KNOX_TOKEN': input("Enter your JWT token: "),
        'SSB_READONLY': 'false',
        'MCP_TRANSPORT': 'stdio',
        'KNOX_VERIFY_SSL': 'true',
        'HTTP_TIMEOUT_SECONDS': '60',
        'PYTHONPATH': '/Users/ibrooks/Documents/GitHub/SSB-MCP-Server/src'
    })
    
    try:
        # Import and test the MCP server
        sys.path.insert(0, '/Users/ibrooks/Documents/GitHub/SSB-MCP-Server/src')
        from ssb_mcp_server.config import ServerConfig
        from ssb_mcp_server.client import SSBClient
        
        print("✅ MCP server modules imported successfully")
        
        # Test configuration
        config = ServerConfig()
        print(f"✅ Configuration loaded: {config.knox_gateway_url}")
        
        # Test client creation
        client = SSBClient(config)
        print("✅ SSB client created successfully")
        
        # Test SSB info
        info = client.get_ssb_info()
        print(f"✅ SSB Info: {info}")
        
        return True
        
    except Exception as e:
        print(f"❌ MCP Server Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Cloud SSB Connection Test")
    print("=" * 50)
    
    # Test 1: Direct API connection
    success1 = test_cloud_ssb_connection()
    
    if success1:
        # Test 2: MCP server integration
        success2 = test_mcp_server_with_cloud_ssb()
        
        if success2:
            print("\n🎉 All tests passed! Cloud SSB is ready for MCP server.")
        else:
            print("\n⚠️  API connection works, but MCP server needs configuration.")
    else:
        print("\n❌ Cloud SSB connection failed. Check credentials and network access.")
    
    sys.exit(0 if success1 else 1)
