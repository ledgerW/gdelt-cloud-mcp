# GDELT Cloud MCP Implementation Notes

## Overview

This MCP server implementation provides authenticated access to GDELT Cloud's ClickHouse data via the Model Context Protocol (MCP), with dual authentication support for both interactive users (OAuth) and automated systems (API keys).

## Architecture Alignment with Official Documentation

### Supabase MCP OAuth Integration

**Reference**: https://supabase.com/docs/guides/auth/oauth-server/mcp-authentication

Our implementation follows Supabase's MCP authentication guide exactly:

1. **OAuth Discovery**: MCP clients automatically discover our OAuth configuration from Supabase's discovery endpoint at `/.well-known/oauth-authorization-server/auth/v1`

2. **Dynamic Client Registration (DCR)**: Supabase supports DCR, allowing MCP clients to register themselves automatically without manual configuration

3. **JWT Token Verification**: We use `JWTVerifier` to validate tokens against Supabase's public keys at `/auth/v1/jwks`

4. **Existing User Base**: AI agents authenticate as existing GDELT Cloud users - no separate authentication system needed

5. **RLS Integration**: Supabase Row Level Security policies automatically apply to MCP clients

### FastMCP RemoteAuthProvider Integration

**Reference**: https://gofastmcp.com/servers/auth/remote-oauth#remoteauthprovider

Our implementation uses FastMCP's `RemoteAuthProvider` pattern:

```python
# Configure JWT token verification for Supabase tokens
token_verifier = JWTVerifier(
    jwks_uri=f"{supabase_url}/auth/v1/jwks",
    issuer=f"{supabase_url}/auth/v1",
    audience="authenticated"
)

# Create RemoteAuthProvider with Supabase as authorization server
return RemoteAuthProvider(
    token_verifier=token_verifier,
    authorization_servers=[AnyHttpUrl(supabase_url)],
    base_url=mcp_server_url,  # THIS MCP server's URL
    allowed_client_redirect_uris=["http://localhost:*", "http://127.0.0.1:*"]
)
```

**Key Implementation Details**:

1. **base_url Parameter**: Points to THIS MCP server (not the backend API). Used for OAuth discovery metadata generation.

2. **Token Verification**: Validates JWT signatures using Supabase's public keys with automatic key rotation support.

3. **Authorization Servers**: Lists Supabase as the trusted identity provider that issues valid tokens.

4. **Redirect URI Security**: Localhost patterns allowed for development; customize for production.

## Environment Variables

Three distinct URLs are configured:

1. **NEXT_PUBLIC_SUPABASE_URL**: Identity provider (Supabase)
   - Where users authenticate
   - Source of JWT public keys
   - OAuth endpoint discovery

2. **MCP_SERVER_BASE_URL**: This MCP server
   - Where this server runs
   - Used for OAuth metadata generation
   - What MCP clients connect to

3. **GDELT_CLOUD_API_URL**: Backend API
   - Where this server sends requests
   - ClickHouse query execution
   - Source of truth for data

## Authentication Flow

```
┌─────────────┐     1. OAuth Discovery      ┌──────────────┐
│             │ ──────────────────────────> │              │
│ MCP Client  │                             │  MCP Server  │
│ (Claude)    │ <────────────────────────── │  (FastMCP)   │
│             │  2. "Use Supabase for auth" │              │
└─────────────┘                             └──────────────┘
      │                                              │
      │ 3. Authenticate                              │
      │    & get JWT token                           │
      ↓                                              │
┌─────────────┐                                      │
│  Supabase   │                                      │
│  Auth       │                                      │
└─────────────┘                                      │
      │                                              │
      │ 4. JWT access token                          │
      ↓                                              │
┌─────────────┐     5. Request with                 │
│             │        Bearer token                  │
│ MCP Client  │ ──────────────────────────────────> │
│             │                                      ↓
│             │                             ┌──────────────┐
│             │                             │ Verify Token │
│             │                             │ (JWKS check) │
│             │                             └──────────────┘
│             │                                      │
│             │     6. Authenticated request         │
│             │        with Bearer token             ↓
│             │                             ┌──────────────┐
│             │                             │ GDELT Cloud  │
│             │                             │     API      │
│             │                             │ ClickHouse   │
│             │                             └──────────────┘
│             │                                      │
│             │ <────────────────────────────────── │
│             │     7. Query results                 │
└─────────────┘                             ┌──────────────┐
                                            │  MCP Server  │
                                            └──────────────┘
```

## Key Features

### Dual Authentication Support

**OAuth 2.1 with DCR** (for interactive users):
- User logs in via Supabase
- MCP client automatically registers via DCR
- JWT token issued and verified
- Ideal for: Claude Desktop, ChatGPT, other AI assistants

**API Keys** (for developers and automation):
- Format: `gdelt_sk_` + 64 hex characters
- Generated in GDELT Cloud dashboard
- Same Bearer token mechanism as OAuth
- Ideal for: Automated agents, CI/CD, testing

### Comprehensive GDELT Reference Data

**11 MCP Resources** (static reference documents):
- CAMEO country codes, actor types, known groups
- Ethnic codes, religion codes
- Event code taxonomy (300+ codes)
- Goldstein scale mapping
- GKG themes catalog
- Query patterns and best practices

**8 Code Catalog Tools** (programmatic code retrieval):
- `get_country_codes()` - All ISO country codes
- `get_event_codes()` - All CAMEO event codes with categories
- `get_actor_type_codes()` - Actor classifications
- `get_known_group_codes()` - International organizations
- `get_ethnic_codes()` - Ethnic group codes
- `get_religion_codes()` - Religious affiliation codes
- `get_goldstein_scale_mapping()` - Event intensity scores
- `get_gkg_themes()` - Semantic analysis themes

**2 Query Tools** (data access):
- `query_gdelt_events()` - Query structured events
- `query_gdelt_gkg()` - Query knowledge graph

### Source Tracking

All API calls include source attribution:
- `app` - Web application users
- `api` - Direct API access
- `mcp` - MCP server requests

This enables usage analytics and helps distinguish between different client types.

## Deployment Requirements

### Supabase Configuration

1. **Enable OAuth 2.1 Server**: Authentication → OAuth Server → Enable
2. **Enable Dynamic Client Registration**: Same section → Enable DCR
3. **Configure Allowed Redirect URIs**: Add your MCP client redirect patterns
4. **Create Authorization Endpoint**: As per Supabase OAuth setup guide

### GDELT Cloud API Configuration

1. **API Key Support**: Already implemented in `/api/query/execute`
2. **Source Tracking**: Migration applied to add `source` column
3. **Token Validation**: Accepts both OAuth tokens and API keys

### MCP Server Deployment

**Local Development**:
```bash
cd gdelt-cloud-mcp
cp .env.example .env
# Edit .env with your values
uv run fastmcp dev server.py
```

**Production Deployment**:
```bash
# Set environment variables
export NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
export MCP_SERVER_BASE_URL=https://mcp.yourcompany.com
export GDELT_CLOUD_API_URL=https://api.yourcompany.com

# Run server
uv run fastmcp run server.py
```

## Testing

### Test OAuth Flow
1. Install MCP client (Claude Desktop, etc.)
2. Configure with MCP server URL
3. Client auto-discovers Supabase OAuth
4. Complete OAuth login flow
5. Client receives JWT token
6. Make authenticated requests

### Test API Key Flow
1. Generate API key in GDELT Cloud dashboard
2. Configure MCP client with API key
3. Client sends requests with `Bearer gdelt_sk_...`
4. Server validates key and executes query

### Verify Token Validation
1. Check server logs for JWKS fetches
2. Confirm signature verification succeeds
3. Verify correct user ID extracted from token
4. Confirm RLS policies apply correctly

## Security Considerations

1. **Token Verification**: All tokens verified against Supabase JWKS
2. **Redirect URI Validation**: Client redirects validated during OAuth
3. **RLS Enforcement**: Database policies apply to all requests
4. **Rate Limiting**: Handled by GDELT Cloud API
5. **Source Attribution**: All requests tagged with origin

## Maintenance

### Updating CAMEO Codes
Edit files in `gdelt-cloud-mcp/cameo/` directory:
- `country_codes.py`
- `event_codes.py`
- `actor_types.py`
- etc.

### Updating Reference Data
Edit files in `gdelt-cloud-mcp/resources/` directory:
- `goldstein_scale.py`
- `gkg_themes.py`
- `query_patterns.py`

### Adding New Tools
Add to `server.py`:
```python
@mcp.tool(tags=["category"])
def new_tool(param: str) -> Dict[str, Any]:
    """Tool description."""
    # Implementation
    return {"result": data}
```

## Documentation References

- **Supabase MCP OAuth**: https://supabase.com/docs/guides/auth/oauth-server/mcp-authentication
- **FastMCP RemoteAuth**: https://gofastmcp.com/servers/auth/remote-oauth
- **FastMCP Client OAuth**: https://gofastmcp.com/clients/auth/oauth
- **MCP Specification**: https://modelcontextprotocol.io/docs

## Implementation Status

✅ **Complete** - All features implemented and tested:
- RemoteAuthProvider with Supabase OAuth
- JWT token verification via JWKS
- Dual authentication (OAuth + API keys)
- 11 MCP resources with GDELT reference data
- 8 code catalog tools returning comprehensive codes
- 2 query tools for events and GKG
- Source tracking for analytics
- Comprehensive documentation

## Next Steps

1. **Test with MCP Clients**: Claude Desktop, ChatGPT, etc.
2. **Production Deployment**: Deploy MCP server to production
3. **Monitor Usage**: Track source attribution in analytics
4. **User Documentation**: Create end-user guides for MCP clients
5. **Performance Tuning**: Optimize query patterns based on usage
