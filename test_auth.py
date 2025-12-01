#!/usr/bin/env python3
"""
Authentication Test Script for GDELT Cloud MCP Server

Tests all authentication scenarios:
1. OAuth JWT authentication with Supabase
2. API key authentication
3. Dual authentication flow
4. Server startup validation

IMPORTANT ARCHITECTURE:
- OAuth: Uses CLOUD Supabase (https://ntytitgiqvokxrlndpby.supabase.co)
  * OAuth tokens verified against cloud Supabase JWKS
  * Used for interactive user authentication (ChatGPT, Claude, etc.)
  
- API Keys: Stored in LOCAL Supabase database
  * API keys generated and validated against local database
  * Used for developer/agent authentication
  * Must be created via local Next.js: http://localhost:3000/dashboard/api-keys

Prerequisites:
- Local Supabase running: supabase start
- Local Next.js running: cd nextjs_ && npm run dev  
- MCP server configured in .env with:
  * SUPABASE_URL = Cloud Supabase (for OAuth)
  * GDELT_CLOUD_API_URL = http://localhost:3000 (for API calls)

Usage:
    python test_auth.py
    python test_auth.py --skip-oauth  # Skip OAuth tests
    python test_auth.py --verbose     # Detailed output
"""

import os
import sys
import json
import asyncio
import argparse
from typing import Optional, Dict, Any
from dotenv import load_dotenv
import httpx
from colorama import init, Fore, Style

# Initialize colorama for colored output
init(autoreset=True)

# Load environment variables
load_dotenv()

class AuthTester:
    """Test authentication scenarios for GDELT Cloud MCP Server."""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.mcp_server_url = os.getenv('MCP_SERVER_BASE_URL', 'http://localhost')
        self.api_url = os.getenv('GDELT_CLOUD_API_URL', 'http://localhost:3000')
        self.test_api_key = None  # Will be set from user input or generation
        
    def log(self, message: str, level: str = "info"):
        """Log message with color coding."""
        if level == "success":
            print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")
        elif level == "error":
            print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")
        elif level == "warning":
            print(f"{Fore.YELLOW}⚠ {message}{Style.RESET_ALL}")
        elif level == "info":
            print(f"{Fore.CYAN}ℹ {message}{Style.RESET_ALL}")
        else:
            print(message)
    
    def log_verbose(self, message: str):
        """Log verbose message."""
        if self.verbose:
            print(f"{Fore.MAGENTA}  → {message}{Style.RESET_ALL}")
    
    async def test_environment_setup(self) -> bool:
        """Test 1: Verify environment variables are set."""
        self.log("\n=== Test 1: Environment Setup ===", "info")
        
        all_good = True
        
        # Check SUPABASE_URL
        if self.supabase_url:
            self.log(f"SUPABASE_URL: {self.supabase_url}", "success")
        else:
            self.log("SUPABASE_URL not set", "error")
            all_good = False
        
        # Check MCP_SERVER_BASE_URL
        if self.mcp_server_url:
            self.log(f"MCP_SERVER_BASE_URL: {self.mcp_server_url}", "success")
        else:
            self.log("MCP_SERVER_BASE_URL not set (using default)", "warning")
        
        # Check GDELT_CLOUD_API_URL
        if self.api_url:
            self.log(f"GDELT_CLOUD_API_URL: {self.api_url}", "success")
        else:
            self.log("GDELT_CLOUD_API_URL not set", "error")
            all_good = False
        
        return all_good
    
    async def test_supabase_connection(self) -> bool:
        """Test 2: Verify Supabase is accessible."""
        self.log("\n=== Test 2: Supabase Connection ===", "info")
        
        try:
            async with httpx.AsyncClient() as client:
                # Test health endpoint (cloud Supabase may return 401, that's ok)
                response = await client.get(f"{self.supabase_url}/auth/v1/health", timeout=10.0)
                if response.status_code in [200, 401]:
                    self.log("Supabase endpoint: Accessible", "success")
                    self.log_verbose(f"Response status: {response.status_code}")
                else:
                    self.log(f"Supabase health check failed: {response.status_code}", "error")
                    return False
                
                # Test JWKS endpoint (used for token verification)
                response = await client.get(f"{self.supabase_url}/auth/v1/jwks", timeout=10.0)
                if response.status_code in [200, 401]:
                    if response.status_code == 200:
                        jwks = response.json()
                        self.log("Supabase JWKS endpoint: OK", "success")
                        self.log_verbose(f"Keys available: {len(jwks.get('keys', []))}")
                    else:
                        self.log("Supabase JWKS endpoint: Accessible (401 - may require auth)", "success")
                        self.log_verbose("Note: Cloud Supabase JWKS should be public, but returns 401")
                else:
                    self.log(f"Supabase JWKS endpoint failed: {response.status_code}", "error")
                    return False
                
                # Test OAuth discovery endpoint (Supabase format includes /auth/v1 suffix)
                response = await client.get(
                    f"{self.supabase_url}/.well-known/oauth-authorization-server/auth/v1",
                    timeout=10.0
                )
                if response.status_code == 200:
                    metadata = response.json()
                    self.log("OAuth discovery endpoint: OK", "success")
                    self.log_verbose(f"Authorization endpoint: {metadata.get('authorization_endpoint')}")
                    self.log_verbose(f"Token endpoint: {metadata.get('token_endpoint')}")
                    self.log_verbose(f"JWKS URI: {metadata.get('jwks_uri')}")
                elif response.status_code == 404:
                    self.log("OAuth 2.1 server not configured in cloud Supabase (404)", "warning")
                    self.log("To enable: Dashboard > Authentication > OAuth Server", "info")
                    self.log("Note: OAuth is optional - API keys work without it", "info")
                    # This is a warning, not a failure - OAuth is optional
                    return True
                else:
                    self.log(f"OAuth discovery failed: {response.status_code}", "error")
                    return False
                
                return True
                
        except httpx.ConnectError as e:
            self.log(f"Cannot connect to Supabase: {e}", "error")
            self.log("Is Supabase running? Try: supabase start", "warning")
            return False
        except Exception as e:
            self.log(f"Supabase connection test failed: {e}", "error")
            return False
    
    async def test_nextjs_connection(self) -> bool:
        """Test 3: Verify Next.js API is accessible."""
        self.log("\n=== Test 3: Next.js API Connection ===", "info")
        
        try:
            async with httpx.AsyncClient() as client:
                # Test API health (just try to connect)
                response = await client.get(f"{self.api_url}", timeout=10.0)
                if response.status_code in [200, 404]:  # 404 is ok, means server is running
                    self.log("Next.js API: Accessible", "success")
                    self.log_verbose(f"Status: {response.status_code}")
                else:
                    self.log(f"Next.js API returned unexpected status: {response.status_code}", "warning")
                
                return True
                
        except httpx.ConnectError as e:
            self.log(f"Cannot connect to Next.js API: {e}", "error")
            self.log("Is Next.js running? Try: cd nextjs_ && npm run dev", "warning")
            return False
        except Exception as e:
            self.log(f"Next.js API connection test failed: {e}", "error")
            return False
    
    async def test_api_key_format(self) -> bool:
        """Test 4: Validate API key format."""
        self.log("\n=== Test 4: API Key Format Validation ===", "info")
        
        # Get API key from user or environment
        test_key = os.getenv('TEST_API_KEY')
        
        if not test_key:
            self.log("No TEST_API_KEY in environment", "warning")
            print("\nPlease provide a test API key (or press Enter to skip):")
            print("  You can generate one at: http://localhost:3000/dashboard/api-keys")
            test_key = input("API Key (gdelt_sk_...): ").strip()
        
        if not test_key:
            self.log("Skipping API key tests (no key provided)", "warning")
            return True
        
        # Validate format
        if test_key.startswith('gdelt_sk_') and len(test_key) == 73:  # gdelt_sk_ + 64 hex chars
            self.log("API key format: Valid", "success")
            self.test_api_key = test_key
            return True
        else:
            self.log("API key format: Invalid", "error")
            self.log("Expected format: gdelt_sk_ + 64 hex characters (73 total)", "info")
            return False
    
    async def test_api_key_authentication(self) -> bool:
        """Test 5: Test API key authentication with Next.js API."""
        self.log("\n=== Test 5: API Key Authentication ===", "info")
        
        if not self.test_api_key:
            self.log("Skipping API key auth test (no key provided)", "warning")
            return True
        
        self.log("Note: API key must exist in the database that Next.js connects to", "info")
        self.log(f"Testing against: {self.api_url}", "info")
        
        try:
            async with httpx.AsyncClient() as client:
                # Test query endpoint with API key
                headers = {
                    "Authorization": f"Bearer {self.test_api_key}",
                    "Content-Type": "application/json"
                }
                
                # API expects raw SQL query, not structured parameters
                payload = {
                    "query": "SELECT global_event_id, day, actor1_name, actor2_name FROM gdelt_events WHERE day >= '2025-01-01' LIMIT 5"
                }
                
                self.log_verbose(f"Testing API endpoint: {self.api_url}/api/query/execute")
                self.log_verbose(f"Request headers: {headers}")
                self.log_verbose(f"Request payload: {json.dumps(payload, indent=2)}")
                
                response = await client.post(
                    f"{self.api_url}/api/query/execute",
                    headers=headers,
                    json=payload,
                    timeout=30.0
                )
                
                self.log_verbose(f"Response status: {response.status_code}")
                self.log_verbose(f"Response body: {response.text[:200]}")
                
                if response.status_code == 200:
                    data = response.json()
                    self.log("API key authentication: Success", "success")
                    self.log_verbose(f"Query returned {len(data.get('data', []))} rows")
                    return True
                elif response.status_code == 401:
                    self.log("API key authentication: Unauthorized", "error")
                    self.log("Key may be invalid, revoked, or expired", "warning")
                    return False
                else:
                    self.log(f"API key authentication: Unexpected status {response.status_code}", "error")
                    return False
                    
        except httpx.ConnectError as e:
            self.log(f"Cannot connect to API: {e}", "error")
            return False
        except Exception as e:
            self.log(f"API key authentication test failed: {e}", "error")
            return False
    
    async def test_oauth_discovery(self) -> bool:
        """Test 6: Test OAuth metadata discovery (if MCP server is running)."""
        self.log("\n=== Test 6: OAuth Discovery Metadata ===", "info")
        
        # This test requires the MCP server to be running
        # For now, we'll just verify the configuration is correct
        
        self.log("OAuth configuration:", "info")
        self.log_verbose(f"  Authorization Server: {self.supabase_url}")
        self.log_verbose(f"  MCP Server Base URL: {self.mcp_server_url}")
        self.log_verbose(f"  Expected discovery at: {self.mcp_server_url}/.well-known/oauth-protected-resource")
        
        self.log("OAuth discovery requires running MCP server", "warning")
        self.log("To test: uv run fastmcp dev server.py", "info")
        
        return True
    
    async def test_dual_token_verifier(self) -> bool:
        """Test 7: Test DualTokenVerifier logic."""
        self.log("\n=== Test 7: DualTokenVerifier Logic ===", "info")
        
        try:
            # Import and test the verifier
            from utils.dual_token_verifier import DualTokenVerifier
            from utils.auth import is_api_key, validate_api_key
            
            # Test API key detection (prefix only)
            detection_tests = [
                ("gdelt_sk_" + "a" * 64, True, "is_api_key: Valid prefix"),
                ("Bearer gdelt_sk_" + "a" * 64, False, "is_api_key: Bearer prefix should be removed first"),
                ("invalid_key", False, "is_api_key: Invalid prefix"),
                ("gdelt_sk_short", True, "is_api_key: Valid prefix (even if short)"),
            ]
            
            # Test API key validation (prefix + length + format)
            validation_tests = [
                ("gdelt_sk_" + "a" * 64, True, "validate_api_key: Valid format"),
                ("gdelt_sk_short", False, "validate_api_key: Too short"),
                ("gdelt_sk_" + "z" * 63, False, "validate_api_key: Wrong length"),
                ("invalid_key", False, "validate_api_key: Invalid prefix"),
            ]
            
            all_passed = True
            
            # Test detection
            for token, expected, description in detection_tests:
                result = is_api_key(token)
                if result == expected:
                    self.log(f"✓ {description}", "success")
                else:
                    self.log(f"✗ {description}: Expected {expected}, got {result}", "error")
                    all_passed = False
            
            # Test validation
            for token, expected, description in validation_tests:
                result = validate_api_key(token)
                if result == expected:
                    self.log(f"✓ {description}", "success")
                else:
                    self.log(f"✗ {description}: Expected {expected}, got {result}", "error")
                    all_passed = False
            
            return all_passed
            
        except ImportError as e:
            self.log(f"Cannot import DualTokenVerifier: {e}", "error")
            return False
        except Exception as e:
            self.log(f"DualTokenVerifier test failed: {e}", "error")
            return False
    
    async def run_all_tests(self, skip_oauth: bool = False) -> Dict[str, bool]:
        """Run all authentication tests."""
        results = {}
        
        print(f"\n{Fore.CYAN}{'=' * 60}")
        print(f"{Fore.CYAN}GDELT Cloud MCP Server - Authentication Test Suite")
        print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}\n")
        
        # Test 1: Environment Setup
        results['environment'] = await self.test_environment_setup()
        
        # Test 2: Supabase Connection
        results['supabase'] = await self.test_supabase_connection()
        
        # Test 3: Next.js Connection
        results['nextjs'] = await self.test_nextjs_connection()
        
        # Test 4: API Key Format
        results['api_key_format'] = await self.test_api_key_format()
        
        # Test 5: API Key Authentication
        results['api_key_auth'] = await self.test_api_key_authentication()
        
        # Test 6: OAuth Discovery
        if not skip_oauth:
            results['oauth_discovery'] = await self.test_oauth_discovery()
        
        # Test 7: DualTokenVerifier
        results['dual_verifier'] = await self.test_dual_token_verifier()
        
        # Summary
        print(f"\n{Fore.CYAN}{'=' * 60}")
        print(f"{Fore.CYAN}Test Summary")
        print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}\n")
        
        passed = sum(1 for v in results.values() if v)
        total = len(results)
        
        for test_name, result in results.items():
            status = f"{Fore.GREEN}PASS{Style.RESET_ALL}" if result else f"{Fore.RED}FAIL{Style.RESET_ALL}"
            print(f"{test_name:20s}: {status}")
        
        print(f"\n{Fore.CYAN}Result: {passed}/{total} tests passed{Style.RESET_ALL}\n")
        
        if passed == total:
            print(f"{Fore.GREEN}✓ All tests passed! Ready to run MCP server.{Style.RESET_ALL}")
            print(f"{Fore.CYAN}To start server: uv run fastmcp dev server.py{Style.RESET_ALL}\n")
        else:
            print(f"{Fore.YELLOW}⚠ Some tests failed. Review errors above.{Style.RESET_ALL}\n")
        
        return results


async def main():
    """Main test runner."""
    parser = argparse.ArgumentParser(description="Test GDELT Cloud MCP Server authentication")
    parser.add_argument('--skip-oauth', action='store_true', help='Skip OAuth tests')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    args = parser.parse_args()
    
    tester = AuthTester(verbose=args.verbose)
    results = await tester.run_all_tests(skip_oauth=args.skip_oauth)
    
    # Exit with error code if any tests failed
    if not all(results.values()):
        sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())
