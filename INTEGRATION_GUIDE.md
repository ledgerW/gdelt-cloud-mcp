# GDELT Cloud MCP Integration Guide

## Overview

The GDELT Cloud MCP server now fully integrates with the GDELT Cloud API's `/api/query/execute` endpoint with dual authentication support (OAuth + API keys) and source tracking.

## Changes Made

### 1. Database Migration: Source Tracking

**File:** `supabase/migrations/20250131000000_add_source_to_usage_logs.sql`

Added `source` column to `usage_logs` table to track the origin of API calls:
- `app` - Web dashboard usage
- `api` - Direct API usage  
- `mcp` - MCP server usage

```sql
alter table usage_logs 
add column source text check (source in ('app', 'api', 'mcp')) default 'app';
```

### 2. API Route: Dual Authentication

**File:** `nextjs_/app/api/query/execute/route.ts`

Enhanced the query execution endpoint with:

#### API Key Authentication
- Checks `Authorization: Bearer gdelt_sk_*` header
- Validates API key format (73 characters: `gdelt_sk_` + 64 hex chars)
- Queries `api_keys` table to verify validity
- Updates `last_used_at` timestamp on use
- Tracks `api_key_id` in usage logs

#### Session Authentication (Existing)
- Maintains existing Supabase session auth for web app
- No breaking changes to current functionality

#### Source Tracking
- Automatically determines source based on auth method:
  - API keys → `mcp` (default for external/MCP usage)
  - Session → `app` (web dashboard)
- Allows explicit `source` override in request body
- Logs source in `usage_logs` for analytics

### 3. MCP API Client: Query Execution API

**File:** `gdelt-cloud-mcp/utils/api_client.py`

Updated to use `/api/query/execute`:

#### Changes:
- Changed endpoint from `/api/clickhouse/query` → `/api/query/execute`
- Sends `source: 'mcp'` in request body for tracking
- Handles GDELT Cloud API response format:
  ```json
  {
    "success": true,
    "data": [...],
    "rowCount": 42,
    "executionTime": 0.123
  }
  ```
- Better error handling for 400 (validation errors) vs 401 (auth errors)
- Removed unused `format` parameter (handled server-side)

## Authentication Flow

### For MCP Server Users

1. **Generate API Key** (one-time):
   ```bash
   # Via web dashboard
   Login → Dashboard → API Keys → Create New Key
   
   # Or via API
   curl -X POST https://gdeltcloud.com/api/keys/generate \
     -H "Authorization: Bearer <session-token>" \
     -H "Content-Type: application/json" \
     -d '{"label": "My MCP Client"}'
   ```

2. **Configure MCP Client**:
   ```python
   import os
   from fastmcp import Client
   from fastmcp.client.auth import BearerAuth
   
   async with Client(
       "https://mcp.gdeltcloud.com",
       auth=BearerAuth(token=os.environ["GDELT_API_KEY"])
   ) as client:
       result = await client.call_tool("query_gdelt_events", {
           "where_clause": "day >= '2025-01-01' AND actor1_country_code = 'USA'",
           "limit": 100
       })
   ```

3. **MCP Server** → **API Route** → **ClickHouse**:
   ```
   MCP Server                    GDELT Cloud API              ClickHouse
   ┌──────────┐                  ┌──────────────┐             ┌──────────┐
   │          │  POST with       │              │  Execute    │          │
   │  Tools   │  API key     →   │  /api/query/ │  validated  │  gdelt_  │
   │          │  gdelt_sk_*      │  execute     │  query  →   │  tables  │
   │          │  + source=mcp    │              │             │          │
   └──────────┘                  └──────────────┘             └──────────┘
                                        ↓
                                  Usage logged with:
                                  - user_id
                                  - api_key_id  
                                  - source: 'mcp'
   ```

## Usage Tracking

All API calls are now logged with source tracking:

```sql
SELECT 
  source,
  COUNT(*) as calls,
  SUM(units) as total_units
FROM usage_logs
WHERE user_id = '<user-id>'
  AND used_at >= NOW() - INTERVAL '30 days'
GROUP BY source;
```

Example output:
```
 source | calls | total_units
--------+-------+-------------
 app    |  1250 |        1250
 api    |   180 |         180
 mcp    |   420 |         420
```

## Security

### API Key Storage
- **DO**: Store in environment variables
- **DO**: Use secrets managers (AWS, GCP, Azure)
- **DON'T**: Commit to version control
- **DON'T**: Include in logs or error messages

### Rate Limiting
Current limits:
- 100,000 API calls per month (Pro plan)
- 100 requests per minute
- 10 concurrent connections

Rate limits are shared across all sources (app, api, mcp).

### Key Management
- Maximum 5 active keys per user
- Keys revoked on plan downgrade
- Immediate revocation via dashboard
- Track `last_used_at` for auditing

## Testing

### 1. Run Database Migration
```bash
cd supabase
npx supabase migration up
```

### 2. Test API Key Authentication
```bash
# Generate a test API key via dashboard first
export GDELT_API_KEY="gdelt_sk_your_key_here"

# Test query execution
curl -X POST https://gdeltcloud.com/api/query/execute \
  -H "Authorization: Bearer $GDELT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "SELECT * FROM gdelt_events WHERE day >= '\''2025-01-01'\'' LIMIT 10",
    "source": "mcp"
  }'
```

Expected response:
```json
{
  "success": true,
  "data": [...],
  "rowCount": 10,
  "executionTime": 0.123
}
```

### 3. Test MCP Server
```bash
cd gdelt-cloud-mcp

# Install dependencies
uv pip install -e .

# Set environment
export GDELT_API_KEY="gdelt_sk_your_key_here"
export GDELT_CLOUD_API_URL="http://localhost:3000"  # or production URL

# Run MCP server
fastmcp run server.py
```

Test with Python client:
```python
import asyncio
from fastmcp import Client
from fastmcp.client.auth import BearerAuth
import os

async def test_mcp():
    async with Client(
        "http://localhost:8000",  # MCP server URL
        auth=BearerAuth(token=os.environ["GDELT_API_KEY"])
    ) as client:
        # Test code catalog tool
        countries = await client.call_tool("get_country_codes")
        print(f"Loaded {countries['count']} country codes")
        
        # Test query tool
        result = await client.call_tool("query_gdelt_events", {
            "where_clause": "day >= '2025-01-01' AND event_root_code = '14'",
            "limit": 5
        })
        print(f"Query returned {result['count']} events")

asyncio.run(test_mcp())
```

### 4. Verify Source Tracking
```sql
-- Check usage logs
SELECT 
  source,
  endpoint,
  status,
  used_at
FROM usage_logs
WHERE user_id = auth.uid()
ORDER BY used_at DESC
LIMIT 10;
```

Should show `source = 'mcp'` for MCP calls.

## Troubleshooting

### "Unauthorized" Error
- **Cause**: Invalid or missing API key
- **Fix**: 
  - Verify API key format: `gdelt_sk_` + 64 hex chars
  - Check key not revoked in dashboard
  - Ensure Pro plan is active

### "Invalid query" Error  
- **Cause**: Query validation failed
- **Common issues**:
  - Missing date filter (required for performance)
  - Invalid SQL syntax
  - Forbidden operations (UPDATE, DELETE, etc.)
- **Fix**: Add date filter like `day >= '2025-01-01'`

### Source Not Tracked
- **Cause**: Migration not applied or using old code
- **Fix**: 
  1. Run migration: `npx supabase migration up`
  2. Verify column exists: `\d usage_logs` in psql
  3. Update code to latest version

## Next Steps

1. **Deploy Migration**: Apply the source tracking migration to production
2. **Test API Keys**: Generate test keys and verify authentication
3. **Update MCP Server**: Deploy updated MCP server code
4. **Monitor Usage**: Watch usage logs for source distribution
5. **Add Analytics**: Build dashboards showing usage by source

## Documentation Links

- [MCP Authentication Guide](./docs/MCP_AUTHENTICATION.md)
- [API Key Usage Guide](./docs/API_KEY_USAGE.md)  
- [Local Testing Guide](./docs/LOCAL_TESTING_GUIDE.md)
- [FastMCP Documentation](https://gofastmcp.com)
- [Supabase OAuth for MCP](https://supabase.com/docs/guides/auth/oauth-server/mcp-authentication)
