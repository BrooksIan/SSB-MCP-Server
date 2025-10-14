#!/usr/bin/env python3
"""
Debug script to test different SSB API endpoints and authentication methods.
"""

import json
import requests
import sys

def test_different_endpoints():
    """Test different possible SSB API endpoints."""
    
    # Use hardcoded values since config is simplified
    knox_url = "https://irb-ssb-test-manager0.cgsi-dem.prep-j1tk.a3.cloudera.site:443"
    jwt_token = "eyJqa3UiOiJodHRwczovL2lyYi1zc2ItdGVzdC1tYW5hZ2VyMC5jZ3NpLWRlbS5wcmVwLWoxdGsuYTMuY2xvdWRlcmEuc2l0ZS9pcmItc3NiLXRlc3QvaG9tZXBhZ2Uva25veHRva2VuL2FwaS92Mi9qd2tzLmpzb24iLCJraWQiOiJ5VTJhOTRvOUtNVXZhalZtQmlhb1o1ajVjVVY2OTA4a09HbmdpbUdOREZNIiwidHlwIjoiSldUIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJpYnJvb2tzIiwiYXVkIjoiY2RwLXByb3h5LXRva2VuIiwiamt1IjoiaHR0cHM6Ly9pcmItc3NiLXRlc3QtbWFuYWdlcjAuY2dzaS1kZW0ucHJlcC1qMXRrLmEzLmNsb3VkZXJhLnNpdGUvaXJiLXNzYi10ZXN0L2hvbWVwYWdlL2tub3h0b2tlbi9hcGkvdjIvandrcy5qc29uIiwia2lkIjoieVUyYTk0bzlLTVV2YWpWbUJpYW9aNWo1Y1VWNjkwOGtPR25naW1HTkRGTSIsImlzcyI6IktOT1hTU08iLCJleHAiOjE3NjA1NTAxMTQsIm1hbmFnZWQudG9rZW4iOiJ0cnVlIiwia25veC5pZCI6ImM1N2UzMGJkLWFhMDUtNDNjMS05M2EwLTY4OWVhODMyNmFjZiJ9.Sie9BIK_hF2b0TT0Tujyd9ISlfe6nIQNC4IYRb9j033SSNZ6Y_TmEL_YYIOjjNnOjXGyzsAMX51AGaB1io9lSo_WE_MJUhTgW_PHkMPD8gVjKSXVxM5lHrsEepjOtmJWvYoUY9Ab47r4Qx4HCjau4_zVE-r6m9HQI2RErO0BXYhjUM88whODtNDr1ZYqhv6gxhREovMSxz3Ju2mlUhzBG-Ojt5DDpKAjCl5QjwF91Q8oMTshyC04PzBLarYC0bcuxWznxpPxlGVvIJxeeyEYms53rjICc9r8RocRszn4HnB0hAY47XyDQRjLv8UbctJTd0oImMMEKv0F3kucSHSSUw"
    
    print("🔍 Debugging SSB API Endpoints")
    print("=" * 50)
    print(f"Knox URL: {knox_url}")
    print(f"JWT Token: {jwt_token[:50]}...")
    
    # Different possible endpoints to try
    endpoints = [
        f"{knox_url}/irb-ssb-test/cdp-proxy-token/ssb-sse-api/",
        f"{knox_url}/irb-ssb-test/cdp-proxy-token/ssb-sse-api/api/v1",
        f"{knox_url}/irb-ssb-test/cdp-proxy-token/ssb-sse-api/api/",
        f"{knox_url}/irb-ssb-test/cdp-proxy-token/ssb-sse-api/api/v1/jobs",
        f"{knox_url}/irb-ssb-test/cdp-proxy/ssb-mve-api/api/v1/info",
        f"{knox_url}/irb-ssb-test/cdp-proxy/ssb-mve-api/api/v1",
        f"{knox_url}/irb-ssb-test/cdp-proxy/ssb-mve-api/api/",
        f"{knox_url}/gateway/irb-ssb-test/cdp-proxy-token/ssb-mve-api/api/v1/info",
        f"{knox_url}/gateway/irb-ssb-test/cdp-proxy/ssb-mve-api/api/v1/info",
        f"{knox_url}/gateway/irb-ssb-test/cdp-proxy/ssb-mve-api/api/v1",
        f"{knox_url}/gateway/irb-ssb-test/cdp-proxy/ssb-mve-api/api/",
    ]
    
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'Content-Type': 'application/json'
    }
    
    for i, endpoint in enumerate(endpoints, 1):
        print(f"\n{i}. Testing: {endpoint}")
        try:
            response = requests.get(endpoint, headers=headers, timeout=10, verify=True)
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print(f"   ✅ SUCCESS! Response: {response.json()}")
                return True
            else:
                print(f"   ❌ Failed: {response.text[:200]}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return False

def test_authentication_methods():
    """Test different authentication methods."""
    
    # Use hardcoded values since config is simplified
    knox_url = "https://irb-ssb-test-manager0.cgsi-dem.prep-j1tk.a3.cloudera.site:443"
    jwt_token = "eyJqa3UiOiJodHRwczovL2lyYi1zc2ItdGVzdC1tYW5hZ2VyMC5jZ3NpLWRlbS5wcmVwLWoxdGsuYTMuY2xvdWRlcmEuc2l0ZS9pcmItc3NiLXRlc3QvaG9tZXBhZ2Uva25veHRva2VuL2FwaS92Mi9qd2tzLmpzb24iLCJraWQiOiJ5VTJhOTRvOUtNVXZhalZtQmlhb1o1ajVjVVY2OTA4a09HbmdpbUdOREZNIiwidHlwIjoiSldUIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJpYnJvb2tzIiwiYXVkIjoiY2RwLXByb3h5LXRva2VuIiwiamt1IjoiaHR0cHM6Ly9pcmItc3NiLXRlc3QtbWFuYWdlcjAuY2dzaS1kZW0ucHJlcC1qMXRrLmEzLmNsb3VkZXJhLnNpdGUvaXJiLXNzYi10ZXN0L2hvbWVwYWdlL2tub3h0b2tlbi9hcGkvdjIvandrcy5qc29uIiwia2lkIjoieVUyYTk0bzlLTVV2YWpWbUJpYW9aNWo1Y1VWNjkwOGtPR25naW1HTkRGTSIsImlzcyI6IktOT1hTU08iLCJleHAiOjE3NjA1NTAxMTQsIm1hbmFnZWQudG9rZW4iOiJ0cnVlIiwia25veC5pZCI6ImM1N2UzMGJkLWFhMDUtNDNjMS05M2EwLTY4OWVhODMyNmFjZiJ9.Sie9BIK_hF2b0TT0Tujyd9ISlfe6nIQNC4IYRb9j033SSNZ6Y_TmEL_YYIOjjNnOjXGyzsAMX51AGaB1io9lSo_WE_MJUhTgW_PHkMPD8gVjKSXVxM5lHrsEepjOtmJWvYoUY9Ab47r4Qx4HCjau4_zVE-r6m9HQI2RErO0BXYhjUM88whODtNDr1ZYqhv6gxhREovMSxz3Ju2mlUhzBG-Ojt5DDpKAjCl5QjwF91Q8oMTshyC04PzBLarYC0bcuxWznxpPxlGVvIJxeeyEYms53rjICc9r8RocRszn4HnB0hAY47XyDQRjLv8UbctJTd0oImMMEKv0F3kucSHSSUw"
    
    print("\n🔐 Testing Different Authentication Methods")
    print("=" * 50)
    
    # Test endpoint (using the most likely one)
    endpoint = f"{knox_url}/irb-ssb-test/cdp-proxy-token/ssb-sse-api/api/v1/info"
    
    # Different auth methods
    auth_methods = [
        ("Bearer Token", {'Authorization': f'Bearer {jwt_token}'}),
        ("Token Header", {'X-Auth-Token': jwt_token}),
        ("Custom Header", {'X-Knox-Token': jwt_token}),
        ("Basic Auth", None, jwt_token),  # This won't work but let's try
    ]
    
    for method_name, headers in auth_methods:
        if headers is None:
            continue
            
        print(f"\nTesting {method_name}:")
        try:
            response = requests.get(endpoint, headers=headers, timeout=10, verify=True)
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print(f"   ✅ SUCCESS with {method_name}!")
                return True
            else:
                print(f"   ❌ Failed: {response.text[:200]}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return False

def test_knox_gateway_info():
    """Test Knox Gateway information endpoints."""
    
    # Use hardcoded values since config is simplified
    knox_url = "https://irb-ssb-test-manager0.cgsi-dem.prep-j1tk.a3.cloudera.site:443"
    
    print("\n🌐 Testing Knox Gateway Information")
    print("=" * 50)
    
    # Test basic Knox Gateway connectivity
    try:
        response = requests.get(knox_url, timeout=10, verify=True)
        print(f"Knox Gateway Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Knox Gateway is accessible")
        else:
            print(f"❌ Knox Gateway error: {response.text[:200]}")
    except Exception as e:
        print(f"❌ Knox Gateway error: {e}")
    
    # Test Knox Gateway info endpoint
    try:
        info_url = f"{knox_url}/gateway/irb-ssb-test/info"
        response = requests.get(info_url, timeout=10, verify=True)
        print(f"Knox Info Status: {response.status_code}")
        if response.status_code == 200:
            print(f"✅ Knox Info: {response.json()}")
        else:
            print(f"❌ Knox Info error: {response.text[:200]}")
    except Exception as e:
        print(f"❌ Knox Info error: {e}")

if __name__ == "__main__":
    print("🚀 SSB API Debug Tool")
    print("=" * 50)
    
    # Test 1: Different endpoints
    success1 = test_different_endpoints()
    
    if not success1:
        # Test 2: Different auth methods
        success2 = test_authentication_methods()
        
        if not success2:
            # Test 3: Knox Gateway info
            test_knox_gateway_info()
    
    if success1:
        print("\n🎉 Found working endpoint!")
    else:
        print("\n❌ No working endpoint found. Check the JWT token and network access.")
