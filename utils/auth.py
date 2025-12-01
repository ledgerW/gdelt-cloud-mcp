"""
Authentication utilities for GDELT Cloud MCP Server
Supports both OAuth 2.1 and API key authentication

Note: Server-side OAuth is configured via FastMCP CLI/config, not programmatically.
This module provides token validation and context management for API calls.
"""

import os
from typing import Optional


def get_auth_token() -> Optional[str]:
    """
    Get authentication token from environment.
    
    For development/testing, set one of:
    - GDELT_API_KEY: API key (gdelt_sk_*)
    - GDELT_OAUTH_TOKEN: OAuth access token
    
    In production, authentication is handled by FastMCP server automatically.
    
    Returns:
        Authentication token (OAuth or API key) or None
    """
    return os.getenv('GDELT_API_KEY') or os.getenv('GDELT_OAUTH_TOKEN')


def validate_api_key(token: str) -> bool:
    """
    Validate API key format.
    
    Args:
        token: Token to validate
    
    Returns:
        True if valid API key format, False otherwise
    """
    # API keys start with 'gdelt_sk_' followed by 64 hex characters
    if not token or not isinstance(token, str):
        return False
    
    if not token.startswith('gdelt_sk_'):
        return False
    
    # Extract the key part after prefix
    key_part = token[9:]  # Skip 'gdelt_sk_'
    
    # Should be 64 hexadecimal characters
    if len(key_part) != 64:
        return False
    
    try:
        int(key_part, 16)  # Validate hexadecimal
        return True
    except ValueError:
        return False


def is_api_key(token: str) -> bool:
    """
    Check if token is an API key (vs OAuth token).
    
    Args:
        token: Token to check
    
    Returns:
        True if token is an API key, False otherwise
    """
    return token and isinstance(token, str) and token.startswith('gdelt_sk_')


class AuthContext:
    """Context manager for authentication state"""
    
    def __init__(self, token: Optional[str] = None):
        """
        Initialize auth context.
        
        Args:
            token: Authentication token (OAuth or API key)
        """
        self.token = token or get_auth_token()
        self.is_authenticated = bool(self.token)
        self.auth_type = 'api_key' if is_api_key(self.token or '') else 'oauth'
    
    def require_auth(self) -> str:
        """
        Require authentication, raise error if not authenticated.
        
        Returns:
            Authentication token
        
        Raises:
            ValueError: If not authenticated
        """
        if not self.is_authenticated or not self.token:
            raise ValueError('Authentication required')
        return self.token
    
    def validate(self) -> bool:
        """
        Validate the current authentication.
        
        Returns:
            True if authentication is valid, False otherwise
        """
        if not self.token:
            return False
        
        if self.auth_type == 'api_key':
            return validate_api_key(self.token)
        
        # For OAuth tokens, we'll validate against the API
        # (actual validation happens when making API calls)
        return True
