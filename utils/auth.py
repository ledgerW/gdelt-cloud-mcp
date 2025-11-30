"""
Authentication utilities for GDELT Cloud MCP Server
Supports both OAuth 2.1 and API key authentication
"""

import os
from typing import Optional
from fastmcp.server.auth import BearerAuth, RemoteOAuthProvider


def get_auth_token() -> Optional[str]:
    """
    Get authentication token from environment or context.
    
    Returns:
        Authentication token (OAuth or API key) or None
    """
    # Try environment variable first (for development/testing)
    token = os.getenv('GDELT_API_KEY') or os.getenv('GDELT_OAUTH_TOKEN')
    return token


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


def create_oauth_provider() -> RemoteOAuthProvider:
    """
    Create OAuth provider for Supabase OAuth server.
    
    Returns:
        RemoteOAuthProvider configured for GDELT Cloud
    """
    # Get Supabase project URL from environment
    supabase_url = os.getenv('SUPABASE_URL', '')
    
    if not supabase_url:
        raise ValueError('SUPABASE_URL environment variable is required for OAuth')
    
    # Create OAuth provider with Supabase endpoints
    provider = RemoteOAuthProvider(
        auth_url=f"{supabase_url}/auth/v1/authorize",
        token_url=f"{supabase_url}/auth/v1/token",
        discovery_url=f"{supabase_url}/.well-known/oauth-authorization-server/auth/v1",
        scopes=['openid', 'email', 'profile']
    )
    
    return provider


def create_bearer_auth(token: Optional[str] = None) -> BearerAuth:
    """
    Create Bearer authentication for API keys.
    
    Args:
        token: Optional API key token (will use env if not provided)
    
    Returns:
        BearerAuth configured with the API key
    """
    auth_token = token or get_auth_token()
    
    if not auth_token:
        raise ValueError('No authentication token provided')
    
    if not is_api_key(auth_token):
        raise ValueError('Token is not a valid API key format')
    
    if not validate_api_key(auth_token):
        raise ValueError('Invalid API key format')
    
    return BearerAuth(token=auth_token)


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
