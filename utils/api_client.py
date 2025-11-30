"""
GDELT Cloud API Client
Handles HTTP requests to GDELT Cloud ClickHouse query endpoints
"""

import os
import httpx
from typing import Dict, Any, Optional, List
from dataclasses import dataclass


@dataclass
class QueryResult:
    """Result from a ClickHouse query"""
    data: List[Dict[str, Any]]
    count: int
    execution_time: Optional[float] = None
    error: Optional[str] = None


class GDELTCloudAPIClient:
    """Client for interacting with GDELT Cloud API"""
    
    def __init__(self, base_url: Optional[str] = None, auth_token: Optional[str] = None):
        """
        Initialize API client.
        
        Args:
            base_url: Base URL for GDELT Cloud API (default from env)
            auth_token: Authentication token (OAuth or API key)
        """
        self.base_url = base_url or os.getenv('GDELT_CLOUD_API_URL', 'https://gdeltcloud.com')
        self.auth_token = auth_token
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
    
    def _get_headers(self) -> Dict[str, str]:
        """Get HTTP headers with authentication"""
        headers = {
            'Content-Type': 'application/json',
        }
        
        if self.auth_token:
            # Support both Bearer token and direct API key
            if self.auth_token.startswith('gdelt_sk_'):
                headers['Authorization'] = f'Bearer {self.auth_token}'
            else:
                headers['Authorization'] = f'Bearer {self.auth_token}'
        
        return headers
    
    async def execute_query(
        self,
        query: str,
        format: str = 'JSONEachRow'
    ) -> QueryResult:
        """
        Execute a ClickHouse SQL query.
        
        Args:
            query: SQL query string (SELECT only)
            format: ClickHouse format (default: JSONEachRow)
        
        Returns:
            QueryResult with data and metadata
        """
        try:
            response = await self.client.post(
                f'{self.base_url}/api/clickhouse/query',
                headers=self._get_headers(),
                json={'query': query, 'format': format}
            )
            
            if response.status_code == 401:
                return QueryResult(
                    data=[],
                    count=0,
                    error='Authentication required. Please provide valid OAuth token or API key.'
                )
            
            if response.status_code != 200:
                error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
                return QueryResult(
                    data=[],
                    count=0,
                    error=error_data.get('error', f'HTTP {response.status_code}: {response.text}')
                )
            
            result = response.json()
            return QueryResult(
                data=result.get('data', []),
                count=result.get('count', 0),
                execution_time=result.get('executionTime')
            )
            
        except httpx.TimeoutException:
            return QueryResult(
                data=[],
                count=0,
                error='Query timeout. Try reducing query scope or adding more specific filters.'
            )
        except Exception as e:
            return QueryResult(
                data=[],
                count=0,
                error=f'Query failed: {str(e)}'
            )
    
    async def query_events(
        self,
        where_clause: Optional[str] = None,
        select_fields: str = '*',
        limit: int = 100,
        order_by: Optional[str] = None
    ) -> QueryResult:
        """
        Query GDELT events table.
        
        Args:
            where_clause: SQL WHERE clause (without WHERE keyword)
            select_fields: Comma-separated field names
            limit: Maximum rows to return (1-1000)
            order_by: ORDER BY clause (without ORDER BY keyword)
        
        Returns:
            QueryResult with events data
        """
        # Build query
        query = f"SELECT {select_fields} FROM gdelt_events"
        
        if where_clause:
            query += f" WHERE {where_clause}"
        
        if order_by:
            query += f" ORDER BY {order_by}"
        else:
            query += " ORDER BY day DESC"
        
        # Enforce limit bounds
        limit = max(1, min(limit, 1000))
        query += f" LIMIT {limit}"
        
        return await self.execute_query(query)
    
    async def query_gkg(
        self,
        where_clause: Optional[str] = None,
        select_fields: str = '*',
        limit: int = 100,
        order_by: Optional[str] = None
    ) -> QueryResult:
        """
        Query GDELT GKG table.
        
        Args:
            where_clause: SQL WHERE clause (without WHERE keyword)
            select_fields: Comma-separated field names
            limit: Maximum rows to return (1-1000)
            order_by: ORDER BY clause (without ORDER BY keyword)
        
        Returns:
            QueryResult with GKG data
        """
        # Build query
        query = f"SELECT {select_fields} FROM gdelt_gkg"
        
        if where_clause:
            query += f" WHERE {where_clause}"
        
        if order_by:
            query += f" ORDER BY {order_by}"
        else:
            query += " ORDER BY date DESC"
        
        # Enforce limit bounds
        limit = max(1, min(limit, 1000))
        query += f" LIMIT {limit}"
        
        return await self.execute_query(query)
    
    async def health_check(self) -> bool:
        """
        Check if API is accessible.
        
        Returns:
            True if API is healthy, False otherwise
        """
        try:
            response = await self.client.get(
                f'{self.base_url}/api/health',
                headers=self._get_headers(),
                timeout=5.0
            )
            return response.status_code == 200
        except Exception:
            return False
