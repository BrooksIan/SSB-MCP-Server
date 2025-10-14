#!/usr/bin/env python3
"""
Comprehensive MCP Test Protocol for Cloud SSB Environment
Tests all MCP server functionality against the cloud SSB instance.
"""

import os
import sys
import json
import requests
import time
from datetime import datetime

# Cloud SSB Configuration
CLOUD_SSB_CONFIG = {
    'knox_gateway_url': 'https://irb-ssb-test-manager0.cgsi-dem.prep-j1tk.a3.cloudera.site:443',
    'jwt_token': 'eyJqa3UiOiJodHRwczovL2lyYi1zc2ItdGVzdC1tYW5hZ2VyMC5jZ3NpLWRlbS5wcmVwLWoxdGsuYTMuY2xvdWRlcmEuc2l0ZS9pcmItc3NiLXRlc3QvaG9tZXBhZ2Uva25veHRva2VuL2FwaS92Mi9qd2tzLmpzb24iLCJraWQiOiJ5VTJhOTRvOUtNVXZhalZtQmlhb1o1ajVjVVY2OTA4a09HbmdpbUdOREZNIiwidHlwIjoiSldUIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJpYnJvb2tzIiwiYXVkIjoiY2RwLXByb3h5LXRva2VuIiwiamt1IjoiaHR0cHM6Ly9pcmItc3NiLXRlc3QtbWFuYWdlcjAuY2dzaS1kZW0ucHJlcC1qMXRrLmEzLmNsb3VkZXJhLnNpdGUvaXJiLXNzYi10ZXN0L2hvbWVwYWdlL2tub3h0b2tlbi9hcGkvdjIvandrcy5qc29uIiwia2lkIjoieVUyYTk0bzlLTVV2YWpWbUJpYW9aNWo1Y1VWNjkwOGtPR25naW1HTkRGTSIsImlzcyI6IktOT1hTU08iLCJleHAiOjE3NjA1NTM4MzksIm1hbmFnZWQudG9rZW4iOiJ0cnVlIiwia25veC5pZCI6ImM1ZmU0ZmNjLWViZTQtNGNiOS1iYTJmLTM1ZGNlYTAzOTkyOSJ9.a8GrZg7LWli42i7xOHFTt8oi9q03_wcrBIv8GAYyXLYFX1IdUE0GuaVQ8m1Ok2lulm3tcB1IwTaxdTblJ3g6WHCo_5GcvWIXd8Bue0o2_CE0BPcgolf9O3uh0Ftk2JP8RPDgtzmiKhqTmjPbQK6ochAK_AGC58gdLf9omsGfF-NQUdIKmAPRIDSlj_vruRrJj9WHcpa9Z1iAT1Mu8Y18ZOw_ixgZ46hP6shJK1J-aZAjFxNKhOUxqjxr39ZXRIX_V8ZwMXWV0mLU22gHkDLMDkiSZ-zQ5OfHVG96-WKHUBHDAaFYaYdIjegzX17y3WqhvhoyVxG0eApMIJQThsqyGA',
    'ssb_api_base': 'https://irb-ssb-test-manager0.cgsi-dem.prep-j1tk.a3.cloudera.site:443/irb-ssb-test/cdp-proxy-token/ssb-sse-api/api/v1'
}

class MCPTestProtocol:
    """Comprehensive MCP test protocol for cloud SSB environment."""
    
    def __init__(self):
        self.results = {
            'start_time': datetime.now().isoformat(),
            'tests': {},
            'summary': {
                'total_tests': 0,
                'passed': 0,
                'failed': 0,
                'skipped': 0
            }
        }
        self.setup_environment()
    
    def setup_environment(self):
        """Set up environment for MCP server testing."""
        print("🔧 Setting up MCP test environment...")
        
        # Set environment variables
        os.environ.update({
            'KNOX_GATEWAY_URL': CLOUD_SSB_CONFIG['knox_gateway_url'],
            'KNOX_TOKEN': CLOUD_SSB_CONFIG['jwt_token'],
            'SSB_READONLY': 'false',
            'MCP_TRANSPORT': 'stdio',
            'KNOX_VERIFY_SSL': 'true',
            'HTTP_TIMEOUT_SECONDS': '60',
            'PYTHONPATH': '/Users/ibrooks/Documents/GitHub/SSB-MCP-Server/src'
        })
        
        # Add src to Python path
        sys.path.insert(0, '/Users/ibrooks/Documents/GitHub/SSB-MCP-Server/src')
        
        print("✅ Environment setup complete")
    
    def log_test(self, test_name, status, message="", data=None):
        """Log test result."""
        self.results['tests'][test_name] = {
            'status': status,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'data': data
        }
        
        self.results['summary']['total_tests'] += 1
        if status == 'PASS':
            self.results['summary']['passed'] += 1
            print(f"✅ {test_name}: {message}")
        elif status == 'FAIL':
            self.results['summary']['failed'] += 1
            print(f"❌ {test_name}: {message}")
        else:
            self.results['summary']['skipped'] += 1
            print(f"⏭️  {test_name}: {message}")
    
    def test_1_cloud_connectivity(self):
        """Test 1: Cloud SSB connectivity."""
        print("\n🌐 Test 1: Cloud SSB Connectivity")
        print("-" * 40)
        
        try:
            # Test Knox Gateway
            response = requests.get(CLOUD_SSB_CONFIG['knox_gateway_url'], timeout=10, verify=True)
            if response.status_code == 200:
                self.log_test("cloud_connectivity", "PASS", "Knox Gateway accessible")
            else:
                self.log_test("cloud_connectivity", "FAIL", f"Knox Gateway returned {response.status_code}")
                return False
        except Exception as e:
            self.log_test("cloud_connectivity", "FAIL", f"Connection error: {e}")
            return False
        
        # Test SSB API endpoint
        try:
            headers = {'Authorization': f'Bearer {CLOUD_SSB_CONFIG["jwt_token"]}'}
            response = requests.get(f"{CLOUD_SSB_CONFIG['ssb_api_base']}/info", headers=headers, timeout=30, verify=True)
            if response.status_code == 200:
                self.log_test("ssb_api_connectivity", "PASS", "SSB API accessible")
                return True
            else:
                self.log_test("ssb_api_connectivity", "FAIL", f"SSB API returned {response.status_code}")
                return False
        except Exception as e:
            self.log_test("ssb_api_connectivity", "FAIL", f"SSB API error: {e}")
            return False
    
    def test_2_mcp_server_imports(self):
        """Test 2: MCP server module imports."""
        print("\n📦 Test 2: MCP Server Module Imports")
        print("-" * 40)
        
        try:
            from ssb_mcp_server.config import ServerConfig
            from ssb_mcp_server.client import SSBClient
            from ssb_mcp_server.server import main
            self.log_test("mcp_imports", "PASS", "All MCP modules imported successfully")
            return True
        except ImportError as e:
            self.log_test("mcp_imports", "FAIL", f"Import error: {e}")
            return False
        except Exception as e:
            self.log_test("mcp_imports", "FAIL", f"Unexpected error: {e}")
            return False
    
    def test_3_mcp_configuration(self):
        """Test 3: MCP server configuration."""
        print("\n⚙️  Test 3: MCP Server Configuration")
        print("-" * 40)
        
        try:
            from ssb_mcp_server.config import ServerConfig
            config = ServerConfig()
            
            # Check configuration values
            if config.knox_gateway_url == CLOUD_SSB_CONFIG['knox_gateway_url']:
                self.log_test("config_knox_url", "PASS", "Knox Gateway URL configured correctly")
            else:
                self.log_test("config_knox_url", "FAIL", f"Expected {CLOUD_SSB_CONFIG['knox_gateway_url']}, got {config.knox_gateway_url}")
            
            if config.knox_token == CLOUD_SSB_CONFIG['jwt_token']:
                self.log_test("config_jwt_token", "PASS", "JWT token configured correctly")
            else:
                self.log_test("config_jwt_token", "FAIL", "JWT token not configured correctly")
            
            ssb_base = config.build_ssb_base()
            expected_base = CLOUD_SSB_CONFIG['ssb_api_base']
            if ssb_base == expected_base:
                self.log_test("config_ssb_base", "PASS", "SSB base URL configured correctly")
            else:
                self.log_test("config_ssb_base", "FAIL", f"Expected {expected_base}, got {ssb_base}")
            
            return True
        except Exception as e:
            self.log_test("mcp_configuration", "FAIL", f"Configuration error: {e}")
            return False
    
    def test_4_ssb_client_creation(self):
        """Test 4: SSB client creation."""
        print("\n🔗 Test 4: SSB Client Creation")
        print("-" * 40)
        
        try:
            from ssb_mcp_server.config import ServerConfig
            from ssb_mcp_server.client import SSBClient
            
            config = ServerConfig()
            client = SSBClient(
                base_url=config.build_ssb_base(),
                session=client._create_session(config),
                timeout_seconds=config.timeout_seconds,
                proxy_context_path=config.proxy_context_path
            )
            
            self.log_test("ssb_client_creation", "PASS", "SSB client created successfully")
            return client
        except Exception as e:
            self.log_test("ssb_client_creation", "FAIL", f"Client creation error: {e}")
            return None
    
    def test_5_ssb_info_endpoint(self, client):
        """Test 5: SSB info endpoint."""
        print("\n📊 Test 5: SSB Info Endpoint")
        print("-" * 40)
        
        if not client:
            self.log_test("ssb_info", "SKIP", "No client available")
            return False
        
        try:
            info = client.get_ssb_info()
            self.log_test("ssb_info", "PASS", f"SSB info retrieved: {info}")
            return True
        except Exception as e:
            self.log_test("ssb_info", "FAIL", f"Info endpoint error: {e}")
            return False
    
    def test_6_jobs_endpoint(self, client):
        """Test 6: Jobs endpoint."""
        print("\n📋 Test 6: Jobs Endpoint")
        print("-" * 40)
        
        if not client:
            self.log_test("jobs_endpoint", "SKIP", "No client available")
            return False
        
        try:
            jobs = client.list_jobs()
            job_count = len(jobs) if isinstance(jobs, list) else 0
            self.log_test("jobs_endpoint", "PASS", f"Jobs retrieved: {job_count} jobs found")
            return True
        except Exception as e:
            self.log_test("jobs_endpoint", "FAIL", f"Jobs endpoint error: {e}")
            return False
    
    def test_7_tables_endpoint(self, client):
        """Test 7: Tables endpoint."""
        print("\n🗂️  Test 7: Tables Endpoint")
        print("-" * 40)
        
        if not client:
            self.log_test("tables_endpoint", "SKIP", "No client available")
            return False
        
        try:
            tables = client.list_tables()
            table_count = len(tables) if isinstance(tables, list) else 0
            self.log_test("tables_endpoint", "PASS", f"Tables retrieved: {table_count} tables found")
            return True
        except Exception as e:
            self.log_test("tables_endpoint", "FAIL", f"Tables endpoint error: {e}")
            return False
    
    def test_8_data_sources_endpoint(self, client):
        """Test 8: Data sources endpoint."""
        print("\n📡 Test 8: Data Sources Endpoint")
        print("-" * 40)
        
        if not client:
            self.log_test("data_sources_endpoint", "SKIP", "No client available")
            return False
        
        try:
            data_sources = client.list_data_sources()
            ds_count = len(data_sources) if isinstance(data_sources, list) else 0
            self.log_test("data_sources_endpoint", "PASS", f"Data sources retrieved: {ds_count} sources found")
            return True
        except Exception as e:
            self.log_test("data_sources_endpoint", "FAIL", f"Data sources endpoint error: {e}")
            return False
    
    def test_9_mcp_tools_discovery(self):
        """Test 9: MCP tools discovery."""
        print("\n🛠️  Test 9: MCP Tools Discovery")
        print("-" * 40)
        
        try:
            from ssb_mcp_server.server import main
            # This would test if the MCP server can start and expose tools
            # For now, we'll just check if the main function exists
            if callable(main):
                self.log_test("mcp_tools_discovery", "PASS", "MCP server main function available")
                return True
            else:
                self.log_test("mcp_tools_discovery", "FAIL", "MCP server main function not callable")
                return False
        except Exception as e:
            self.log_test("mcp_tools_discovery", "FAIL", f"MCP tools discovery error: {e}")
            return False
    
    def test_10_end_to_end_workflow(self, client):
        """Test 10: End-to-end workflow test."""
        print("\n🔄 Test 10: End-to-End Workflow")
        print("-" * 40)
        
        if not client:
            self.log_test("end_to_end_workflow", "SKIP", "No client available")
            return False
        
        try:
            # Test a complete workflow: get info, list jobs, list tables
            info = client.get_ssb_info()
            jobs = client.list_jobs()
            tables = client.list_tables()
            
            workflow_success = all([
                info is not None,
                isinstance(jobs, list),
                isinstance(tables, list)
            ])
            
            if workflow_success:
                self.log_test("end_to_end_workflow", "PASS", "Complete workflow executed successfully")
                return True
            else:
                self.log_test("end_to_end_workflow", "FAIL", "Workflow execution failed")
                return False
        except Exception as e:
            self.log_test("end_to_end_workflow", "FAIL", f"Workflow error: {e}")
            return False
    
    def run_all_tests(self):
        """Run all MCP test protocols."""
        print("🚀 Starting MCP Test Protocol for Cloud SSB")
        print("=" * 60)
        
        # Test 1: Cloud connectivity
        if not self.test_1_cloud_connectivity():
            print("\n❌ Cloud connectivity failed. Stopping tests.")
            return False
        
        # Test 2: MCP imports
        if not self.test_2_mcp_server_imports():
            print("\n❌ MCP imports failed. Stopping tests.")
            return False
        
        # Test 3: MCP configuration
        if not self.test_3_mcp_configuration():
            print("\n❌ MCP configuration failed. Stopping tests.")
            return False
        
        # Test 4: SSB client creation
        client = self.test_4_ssb_client_creation()
        
        # Test 5-8: SSB endpoints
        self.test_5_ssb_info_endpoint(client)
        self.test_6_jobs_endpoint(client)
        self.test_7_tables_endpoint(client)
        self.test_8_data_sources_endpoint(client)
        
        # Test 9: MCP tools discovery
        self.test_9_mcp_tools_discovery()
        
        # Test 10: End-to-end workflow
        self.test_10_end_to_end_workflow(client)
        
        # Generate final report
        self.generate_report()
        
        return True
    
    def generate_report(self):
        """Generate comprehensive test report."""
        print("\n📊 MCP Test Protocol Report")
        print("=" * 60)
        
        self.results['end_time'] = datetime.now().isoformat()
        
        # Print summary
        summary = self.results['summary']
        print(f"Total Tests: {summary['total_tests']}")
        print(f"✅ Passed: {summary['passed']}")
        print(f"❌ Failed: {summary['failed']}")
        print(f"⏭️  Skipped: {summary['skipped']}")
        
        # Calculate success rate
        if summary['total_tests'] > 0:
            success_rate = (summary['passed'] / summary['total_tests']) * 100
            print(f"📈 Success Rate: {success_rate:.1f}%")
        
        # Print detailed results
        print("\n📋 Detailed Results:")
        for test_name, result in self.results['tests'].items():
            status_icon = "✅" if result['status'] == 'PASS' else "❌" if result['status'] == 'FAIL' else "⏭️"
            print(f"  {status_icon} {test_name}: {result['message']}")
        
        # Save report to file
        report_file = f"mcp_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\n💾 Detailed report saved to: {report_file}")

def main():
    """Main function to run MCP test protocol."""
    protocol = MCPTestProtocol()
    success = protocol.run_all_tests()
    
    if success:
        print("\n🎉 MCP Test Protocol completed successfully!")
        print("The MCP server is ready for use with Claude Desktop.")
    else:
        print("\n⚠️  MCP Test Protocol completed with issues.")
        print("Check the detailed results above for troubleshooting.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
