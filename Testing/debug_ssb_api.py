#!/usr/bin/env python3
"""
Debug script to test different SSB API endpoints and authentication methods.
"""

import json
import requests
import sys
import os

# Add config to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'config'))

from config_loader import ConfigLoader

def test_different_endpoints():
    """Test different possible SSB API endpoints."""
    
    # Load Cloud SSB configuration
    config_loader = ConfigLoader()
    cloud_config = config_loader.get_cloud_ssb_config()
    
    knox_url = cloud_config.get('knox_gateway_url')
    jwt_token = cloud_config.get('jwt_token')
    
    print("🔍 Debugging SSB API Endpoints")
    print("=" * 50)
    print(f"Knox URL: {knox_url}")
    print(f"JWT Token: {jwt_token[:50]}...")
    
    # Different possible endpoints to try
    endpoints = [
        f"{knox_url}/irb-ssb-test/cdp-proxy-token/ssb-sse-api/",
        f"{knox_url}/irb-ssb-test/cdp-proxy-token/ssb-sse-api/api/v1",
        f"{knox_url}/irb-ssb-test/cdp-proxy-token/ssb-sse-api/api/",
        f"{knox_url}/irb-ssb-test/cdp-proxy-token/ssb-sse-api/api/v1/tables",
        f"{knox_url}/irb-ssb-test/cdp-proxy-token/ssb-sse-api/api/v1/jobs",
        f"{knox_url}/irb-ssb-test/cdp-proxy-token/ssb-sse-api/api/v2/projects",
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
    
    successful_endpoints = []
    
    for i, endpoint in enumerate(endpoints, 1):
        print(f"\n{i}. Testing: {endpoint}")
        try:
            response = requests.get(endpoint, headers=headers, timeout=10, verify=True)
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print(f"   ✅ SUCCESS! Response: {response.json()}")
                successful_endpoints.append(endpoint)
            else:
                print(f"   ❌ Failed: {response.text[:200]}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    if successful_endpoints:
        print(f"\n🎉 Found {len(successful_endpoints)} working endpoint(s):")
        for endpoint in successful_endpoints:
            print(f"   ✅ {endpoint}")
        return True
    else:
        print("\n❌ No working endpoints found")
        return False

def test_authentication_methods():
    """Test different authentication methods."""
    
    # Load Cloud SSB configuration
    config_loader = ConfigLoader()
    cloud_config = config_loader.get_cloud_ssb_config()
    
    knox_url = cloud_config.get('knox_gateway_url')
    jwt_token = cloud_config.get('jwt_token')
    
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
    
    # Load Cloud SSB configuration
    config_loader = ConfigLoader()
    cloud_config = config_loader.get_cloud_ssb_config()
    
    knox_url = cloud_config.get('knox_gateway_url')
    
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
    print("\n" + "="*60)
    print("TEST 1: Testing Different Endpoints")
    print("="*60)
    success1 = test_different_endpoints()
    
    # Test 2: Different auth methods
    print("\n" + "="*60)
    print("TEST 2: Testing Different Authentication Methods")
    print("="*60)
    success2 = test_authentication_methods()
    
    # Test 3: Knox Gateway info
    print("\n" + "="*60)
    print("TEST 3: Testing Knox Gateway Information")
    print("="*60)
    test_knox_gateway_info()
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    if success1:
        print("✅ Found working endpoint(s) in Test 1!")
    if success2:
        print("✅ Found working authentication method in Test 2!")
    if not success1 and not success2:
        print("❌ No working endpoints or authentication methods found.")
        print("   Check the JWT token and network access.")
