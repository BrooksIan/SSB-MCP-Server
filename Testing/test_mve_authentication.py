#!/usr/bin/env python3
"""
MVE (Materialized View Engine) Authentication Test Suite
======================================================

This test suite analyzes the root cause of authentication issues with the SSB MVE API.
The MVE API appears to use a completely different authentication system than the main SSB API.

Root Cause Analysis:
- Different Auth Method: MVE API doesn't use Bearer tokens or standard HTTP auth
- API Key Configuration: The API key might need to be configured differently in the SSB UI
- Endpoint Requirements: The MVE API might require additional headers or different URL structure

Author: SSB-MCP-Server
Date: 2025-10-15
"""

import os
import sys
import requests
import json
import time
from typing import Dict, List, Any, Optional

# Add parent directory to Python path to access config module
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from config.config_loader import ConfigLoader

class MVEAuthenticationTester:
    """Test suite for MVE API authentication analysis."""
    
    def __init__(self):
        """Initialize the MVE authentication tester."""
        self.config = ConfigLoader()
        self.knox_url = self.config.get_knox_gateway_url()
        self.jwt_token = self.config.get_jwt_token()
        self.base_url = f"{self.knox_url}/gateway/irb-ssb-test/cdp-proxy/ssb-mve-api/api"
        self.test_results = []
        
    def log_test(self, test_name: str, success: bool, details: str = "", response_data: Any = None):
        """Log test results."""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"    Details: {details}")
        if response_data:
            print(f"    Response: {response_data}")
        
        self.test_results.append({
            'test': test_name,
            'success': success,
            'details': details,
            'response': response_data
        })
        print()
    
    def test_1_mve_endpoint_discovery(self) -> bool:
        """Test 1: Discover MVE API endpoints and structure."""
        print("=" * 60)
        print("TEST 1: MVE Endpoint Discovery")
        print("=" * 60)
        
        try:
            # Test different MVE API base endpoints
            endpoints_to_test = [
                f"{self.base_url}/v1",
                f"{self.base_url}/v1/query",
                f"{self.base_url}/query",
                f"{self.base_url}/api/v1",
                f"{self.base_url}/api/v1/query"
            ]
            
            headers = {
                'Authorization': f'Bearer {self.jwt_token}',
                'Content-Type': 'application/json'
            }
            
            working_endpoints = []
            
            for endpoint in endpoints_to_test:
                try:
                    response = requests.get(endpoint, headers=headers, verify=False, timeout=10)
                    print(f"Testing endpoint: {endpoint}")
                    print(f"  Status: {response.status_code}")
                    
                    if response.status_code == 200:
                        working_endpoints.append(endpoint)
                        print(f"  ✅ Working endpoint found!")
                    elif response.status_code == 401:
                        print(f"  🔐 Requires authentication")
                    elif response.status_code == 404:
                        print(f"  ❌ Not found")
                    else:
                        print(f"  ⚠️  Unexpected status: {response.text[:100]}")
                        
                except Exception as e:
                    print(f"  ❌ Error: {e}")
            
            success = len(working_endpoints) > 0
            details = f"Found {len(working_endpoints)} working endpoints: {working_endpoints}"
            self.log_test("MVE Endpoint Discovery", success, details, working_endpoints)
            return success
            
        except Exception as e:
            self.log_test("MVE Endpoint Discovery", False, f"Error: {e}")
            return False
    
    def test_2_authentication_methods(self) -> bool:
        """Test 2: Test different authentication methods for MVE API."""
        print("=" * 60)
        print("TEST 2: Authentication Methods Analysis")
        print("=" * 60)
        
        # Test URL with known job and MV
        test_url = f"{self.base_url}/v1/query/5202/testMV123?key=7ba11aa3-6df2-4d19-bb02-86da4f7a9d9d&limit=100"
        
        auth_methods = [
            {
                'name': 'Bearer Token',
                'headers': {
                    'Authorization': f'Bearer {self.jwt_token}',
                    'Content-Type': 'application/json'
                }
            },
            {
                'name': 'API Key in X-API-Key Header',
                'headers': {
                    'X-API-Key': '7ba11aa3-6df2-4d19-bb02-86da4f7a9d9d',
                    'Content-Type': 'application/json'
                }
            },
            {
                'name': 'API Key in Authorization Header',
                'headers': {
                    'Authorization': '7ba11aa3-6df2-4d19-bb02-86da4f7a9d9d',
                    'Content-Type': 'application/json'
                }
            },
            {
                'name': 'Basic Auth',
                'headers': {
                    'Authorization': 'Basic aWJyb29rczppYnJvb2tz',  # ibrooks:ibrooks
                    'Content-Type': 'application/json'
                }
            },
            {
                'name': 'API Key in Custom Header',
                'headers': {
                    'X-API-KEY': '7ba11aa3-6df2-4d19-bb02-86da4f7a9d9d',
                    'Content-Type': 'application/json'
                }
            },
            {
                'name': 'Multiple Headers',
                'headers': {
                    'Authorization': f'Bearer {self.jwt_token}',
                    'X-API-Key': '7ba11aa3-6df2-4d19-bb02-86da4f7a9d9d',
                    'Content-Type': 'application/json'
                }
            },
            {
                'name': 'No Auth Headers (API key in URL only)',
                'headers': {
                    'Content-Type': 'application/json'
                }
            }
        ]
        
        successful_methods = []
        
        for method in auth_methods:
            try:
                print(f"Testing: {method['name']}")
                response = requests.get(test_url, headers=method['headers'], verify=False, timeout=10)
                print(f"  Status: {response.status_code}")
                
                if response.status_code == 200:
                    successful_methods.append(method['name'])
                    print(f"  ✅ SUCCESS!")
                    try:
                        data = response.json()
                        print(f"  Response: {json.dumps(data, indent=2)[:200]}...")
                    except:
                        print(f"  Response Text: {response.text[:200]}...")
                elif response.status_code == 401:
                    print(f"  🔐 Unauthorized")
                elif response.status_code == 403:
                    print(f"  🚫 Forbidden")
                elif response.status_code == 404:
                    print(f"  ❌ Not Found")
                else:
                    print(f"  ⚠️  Status {response.status_code}: {response.text[:100]}")
                    
            except Exception as e:
                print(f"  ❌ Error: {e}")
            
            print()
        
        success = len(successful_methods) > 0
        details = f"Successful methods: {successful_methods}" if successful_methods else "No successful authentication methods found"
        self.log_test("Authentication Methods Analysis", success, details, successful_methods)
        return success
    
    def test_3_url_structure_analysis(self) -> bool:
        """Test 3: Analyze different URL structures for MVE API."""
        print("=" * 60)
        print("TEST 3: URL Structure Analysis")
        print("=" * 60)
        
        # Test different URL patterns
        base_patterns = [
            f"{self.knox_url}/gateway/irb-ssb-test/cdp-proxy/ssb-mve-api/api",
            f"{self.knox_url}/gateway/irb-ssb-test/cdp-proxy-api/ssb-mve-api/api",
            f"{self.knox_url}/gateway/irb-ssb-test/ssb-mve-api/api",
            f"{self.knox_url}/irb-ssb-test/cdp-proxy/ssb-mve-api/api",
            f"{self.knox_url}/irb-ssb-test/cdp-proxy-api/ssb-mve-api/api"
        ]
        
        path_patterns = [
            "/v1/query/5202/testMV123",
            "/query/5202/testMV123",
            "/api/v1/query/5202/testMV123",
            "/api/query/5202/testMV123"
        ]
        
        query_params = [
            "?key=7ba11aa3-6df2-4d19-bb02-86da4f7a9d9d&limit=100",
            "?api_key=7ba11aa3-6df2-4d19-bb02-86da4f7a9d9d&limit=100",
            "?token=7ba11aa3-6df2-4d19-bb02-86da4f7a9d9d&limit=100",
            "?key=7ba11aa3-6df2-4d19-bb02-86da4f7a9d9d",
            ""
        ]
        
        working_urls = []
        headers = {
            'Authorization': f'Bearer {self.jwt_token}',
            'Content-Type': 'application/json'
        }
        
        for base in base_patterns:
            for path in path_patterns:
                for query in query_params:
                    test_url = f"{base}{path}{query}"
                    
                    try:
                        response = requests.get(test_url, headers=headers, verify=False, timeout=5)
                        print(f"Testing: {test_url}")
                        print(f"  Status: {response.status_code}")
                        
                        if response.status_code == 200:
                            working_urls.append(test_url)
                            print(f"  ✅ Working URL found!")
                        elif response.status_code == 401:
                            print(f"  🔐 Requires auth")
                        elif response.status_code == 404:
                            print(f"  ❌ Not found")
                        else:
                            print(f"  ⚠️  Status {response.status_code}")
                            
                    except Exception as e:
                        print(f"  ❌ Error: {e}")
                    
                    print()
        
        success = len(working_urls) > 0
        details = f"Found {len(working_urls)} working URLs" if working_urls else "No working URL patterns found"
        self.log_test("URL Structure Analysis", success, details, working_urls)
        return success
    
    def test_4_headers_analysis(self) -> bool:
        """Test 4: Analyze different header combinations for MVE API."""
        print("=" * 60)
        print("TEST 4: Headers Analysis")
        print("=" * 60)
        
        test_url = f"{self.base_url}/v1/query/5202/testMV123?key=7ba11aa3-6df2-4d19-bb02-86da4f7a9d9d&limit=100"
        
        header_combinations = [
            {
                'name': 'Standard SSB Headers',
                'headers': {
                    'Authorization': f'Bearer {self.jwt_token}',
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            },
            {
                'name': 'MVE Specific Headers',
                'headers': {
                    'Authorization': f'Bearer {self.jwt_token}',
                    'Content-Type': 'application/json',
                    'X-API-Key': '7ba11aa3-6df2-4d19-bb02-86da4f7a9d9d',
                    'X-Requested-With': 'XMLHttpRequest'
                }
            },
            {
                'name': 'CDP Headers',
                'headers': {
                    'Authorization': f'Bearer {self.jwt_token}',
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CDP-API-Key': '7ba11aa3-6df2-4d19-bb02-86da4f7a9d9d'
                }
            },
            {
                'name': 'Knox Gateway Headers',
                'headers': {
                    'Authorization': f'Bearer {self.jwt_token}',
                    'Content-Type': 'application/json',
                    'X-Knox-Gateway': 'irb-ssb-test',
                    'X-API-Key': '7ba11aa3-6df2-4d19-bb02-86da4f7a9d9d'
                }
            },
            {
                'name': 'Minimal Headers',
                'headers': {
                    'Content-Type': 'application/json'
                }
            },
            {
                'name': 'Custom MVE Headers',
                'headers': {
                    'Content-Type': 'application/json',
                    'X-MVE-API-Key': '7ba11aa3-6df2-4d19-bb02-86da4f7a9d9d',
                    'X-MVE-Job-ID': '5202',
                    'X-MVE-Endpoint': 'testMV123'
                }
            }
        ]
        
        successful_combinations = []
        
        for combo in header_combinations:
            try:
                print(f"Testing: {combo['name']}")
                response = requests.get(test_url, headers=combo['headers'], verify=False, timeout=10)
                print(f"  Status: {response.status_code}")
                
                if response.status_code == 200:
                    successful_combinations.append(combo['name'])
                    print(f"  ✅ SUCCESS!")
                    try:
                        data = response.json()
                        print(f"  Response: {json.dumps(data, indent=2)[:200]}...")
                    except:
                        print(f"  Response Text: {response.text[:200]}...")
                elif response.status_code == 401:
                    print(f"  🔐 Unauthorized")
                elif response.status_code == 403:
                    print(f"  🚫 Forbidden")
                else:
                    print(f"  ⚠️  Status {response.status_code}: {response.text[:100]}")
                    
            except Exception as e:
                print(f"  ❌ Error: {e}")
            
            print()
        
        success = len(successful_combinations) > 0
        details = f"Successful combinations: {successful_combinations}" if successful_combinations else "No successful header combinations found"
        self.log_test("Headers Analysis", success, details, successful_combinations)
        return success
    
    def test_5_job_state_analysis(self) -> bool:
        """Test 5: Analyze job state requirements for MVE access."""
        print("=" * 60)
        print("TEST 5: Job State Analysis")
        print("=" * 60)
        
        try:
            from src.ssb_mcp_server.config import ServerConfig
            from src.ssb_mcp_server.server import build_client
            
            config = ServerConfig()
            client = build_client(config)
            
            # Get all jobs and their states
            streams = client.list_streams()
            
            if 'jobs' in streams:
                print("Job States Analysis:")
                print("-" * 40)
                
                for job in streams['jobs']:
                    name = job.get('name', 'N/A')
                    job_id = job.get('job_id', 'N/A')
                    state = job.get('state', 'N/A')
                    flink_job_id = job.get('flink_job_id', 'N/A')
                    mv_endpoints = job.get('mv_endpoints', [])
                    
                    print(f"Job: {name} (ID: {job_id})")
                    print(f"  State: {state}")
                    print(f"  Flink Job ID: {flink_job_id}")
                    print(f"  MV Endpoints: {len(mv_endpoints)}")
                    
                    if mv_endpoints:
                        for mv in mv_endpoints:
                            print(f"    - {mv.get('endpoint')}")
                    
                    print()
                
                # Test MVE access for different job states
                test_url = f"{self.base_url}/v1/query/5202/testMV123?key=7ba11aa3-6df2-4d19-bb02-86da4f7a9d9d&limit=100"
                headers = {
                    'Authorization': f'Bearer {self.jwt_token}',
                    'Content-Type': 'application/json'
                }
                
                print("Testing MVE access with current job state...")
                try:
                    response = requests.get(test_url, headers=headers, verify=False, timeout=10)
                    print(f"  Status: {response.status_code}")
                    
                    if response.status_code == 200:
                        print(f"  ✅ MVE accessible with current job state!")
                        success = True
                    else:
                        print(f"  ❌ MVE not accessible: {response.text[:100]}")
                        success = False
                except Exception as e:
                    print(f"  ❌ Error: {e}")
                    success = False
                
                details = f"Job state analysis completed. MVE access: {'Success' if success else 'Failed'}"
                self.log_test("Job State Analysis", success, details)
                return success
            else:
                self.log_test("Job State Analysis", False, "No jobs found")
                return False
                
        except Exception as e:
            self.log_test("Job State Analysis", False, f"Error: {e}")
            return False
    
    def test_6_api_key_validation(self) -> bool:
        """Test 6: Validate API key format and requirements."""
        print("=" * 60)
        print("TEST 6: API Key Validation")
        print("=" * 60)
        
        # Test different API key formats
        api_keys = [
            '7ba11aa3-6df2-4d19-bb02-86da4f7a9d9d',  # Original
            'a7bf2de2-57a2-4f11-ae74-20f5ae00a06f',  # New key
            'test-key-123',
            '5202',  # Job ID as key
            'testMV123',  # MV name as key
            ''  # Empty key
        ]
        
        test_url_base = f"{self.base_url}/v1/query/5202/testMV123"
        headers = {
            'Authorization': f'Bearer {self.jwt_token}',
            'Content-Type': 'application/json'
        }
        
        working_keys = []
        
        for api_key in api_keys:
            test_url = f"{test_url_base}?key={api_key}&limit=100"
            
            try:
                print(f"Testing API key: {api_key}")
                response = requests.get(test_url, headers=headers, verify=False, timeout=5)
                print(f"  Status: {response.status_code}")
                
                if response.status_code == 200:
                    working_keys.append(api_key)
                    print(f"  ✅ Working API key!")
                elif response.status_code == 401:
                    print(f"  🔐 Invalid key")
                elif response.status_code == 403:
                    print(f"  🚫 Forbidden")
                else:
                    print(f"  ⚠️  Status {response.status_code}: {response.text[:50]}")
                    
            except Exception as e:
                print(f"  ❌ Error: {e}")
            
            print()
        
        success = len(working_keys) > 0
        details = f"Working API keys: {working_keys}" if working_keys else "No working API keys found"
        self.log_test("API Key Validation", success, details, working_keys)
        return success
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all MVE authentication tests."""
        print("MVE Authentication Test Suite")
        print("=" * 60)
        print("Analyzing root cause of MVE API authentication issues...")
        print()
        
        start_time = time.time()
        
        # Run all tests
        test_results = {
            'endpoint_discovery': self.test_1_mve_endpoint_discovery(),
            'authentication_methods': self.test_2_authentication_methods(),
            'url_structure': self.test_3_url_structure_analysis(),
            'headers_analysis': self.test_4_headers_analysis(),
            'job_state_analysis': self.test_5_job_state_analysis(),
            'api_key_validation': self.test_6_api_key_validation()
        }
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Summary
        print("=" * 60)
        print("MVE AUTHENTICATION TEST SUMMARY")
        print("=" * 60)
        
        passed_tests = sum(1 for result in test_results.values() if result)
        total_tests = len(test_results)
        
        print(f"Tests Passed: {passed_tests}/{total_tests}")
        print(f"Duration: {duration:.2f} seconds")
        print()
        
        for test_name, result in test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} {test_name.replace('_', ' ').title()}")
        
        print()
        
        if passed_tests == 0:
            print("🔍 ROOT CAUSE ANALYSIS:")
            print("All authentication methods failed, suggesting:")
            print("1. MVE API uses completely different authentication system")
            print("2. API key may need to be configured in SSB UI first")
            print("3. MVE API may require different endpoint structure")
            print("4. Additional headers or authentication flow may be required")
            print("5. MVE API may not be accessible via external API calls")
        elif passed_tests < total_tests:
            print("🔍 PARTIAL SUCCESS:")
            print("Some authentication methods work, indicating:")
            print("1. MVE API is accessible but requires specific configuration")
            print("2. Certain headers or URL patterns are required")
            print("3. API key format or placement may be critical")
        else:
            print("🎉 ALL TESTS PASSED:")
            print("MVE API authentication is working correctly!")
        
        return {
            'test_results': test_results,
            'summary': {
                'passed': passed_tests,
                'total': total_tests,
                'duration': duration,
                'success_rate': (passed_tests / total_tests) * 100
            },
            'detailed_results': self.test_results
        }

def main():
    """Main function to run MVE authentication tests."""
    try:
        tester = MVEAuthenticationTester()
        results = tester.run_all_tests()
        
        # Save results to file
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        results_file = f"mve_auth_test_results_{timestamp}.json"
        
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\\n📊 Detailed results saved to: {results_file}")
        
        return results
        
    except Exception as e:
        print(f"❌ Error running MVE authentication tests: {e}")
        return None

if __name__ == "__main__":
    main()
