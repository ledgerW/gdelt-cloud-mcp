"""
Dual Token Verifier for GDELT Cloud MCP Server
Handles both OAuth JWT tokens (from Supabase) and API keys (gdelt_sk_*)

This enables two authentication flows:
1. OAuth 2.1 with DCR - For interactive users (ChatGPT, Claude Desktop)
2. API Keys - For automated agents and developers
"""

from typing import Optional
from fastmcp.server.auth.providers.jwt import JWTVerifier
from mcp.server.auth.provider import AccessToken
from .auth import is_api_key, validate_api_key


class DualTokenVerifier:
    """
    Token verifier that accepts both OAuth JWT tokens and API keys.
    
    For MCP clients, this enables two authentication paths:
    - OAuth flow: Client authenticates user via Supabase, gets JWT token
    - API key flow: Client provides API key directly (gdelt_sk_*)
    
    Both token types are passed as Bearer tokens in the Authorization header.
    """
    
    def __init__(self, jwt_verifier: JWTVerifier):
        """
        Initialize dual token verifier.
        
        Args:
            jwt_verifier: JWTVerifier instance configured for Supabase OAuth tokens
        """
        self.jwt_verifier = jwt_verifier
    
    async def verify_token(self, token: str) -> Optional[AccessToken]:
        """
        Verify a token (either JWT or API key).
        
        Args:
            token: Bearer token from Authorization header
        
        Returns:
            AccessToken object with verified token info
            
        Raises:
            Exception: If token verification fails
        """
        # Check if it's an API key
        if is_api_key(token):
            return await self._verify_api_key(token)
        
        # Otherwise, treat as OAuth JWT token
        return await self.jwt_verifier.verify_token(token)
    
    async def _verify_api_key(self, token: str) -> AccessToken:
        """
        Verify API key format (actual validation happens in GDELT Cloud API).
        
        The MCP server only validates the FORMAT of API keys here.
        The actual key validity is checked by the GDELT Cloud API when
        the MCP server forwards requests with the Bearer token.
        
        Args:
            token: API key to verify
        
        Returns:
            AccessToken object with API key info
            
        Raises:
            ValueError: If API key format is invalid
        """
        if not validate_api_key(token):
            raise ValueError(f"Invalid API key format. Must be 'gdelt_sk_' + 64 hex chars")
        
        # Return AccessToken object for API keys
        # The actual user_id and permissions will be validated by GDELT Cloud API
        return AccessToken(
            token=token,
            client_id="api_key_client",  # Placeholder client ID for API keys
            scopes=["read", "write"],    # Default scopes for API keys
            expires_at=None,              # API keys don't expire (managed via revocation)
            resource=None
        )
    
    @property
    def jwks_uri(self) -> str:
        """Get JWKS URI from underlying JWT verifier."""
        return self.jwt_verifier.jwks_uri
    
    @property
    def issuer(self) -> str:
        """Get issuer from underlying JWT verifier."""
        return self.jwt_verifier.issuer
    
    @property
    def audience(self) -> Optional[str]:
        """Get audience from underlying JWT verifier."""
        return self.jwt_verifier.audience
    
    @property
    def required_scopes(self) -> Optional[list]:
        """Get required scopes from underlying JWT verifier."""
        return getattr(self.jwt_verifier, 'required_scopes', None)
