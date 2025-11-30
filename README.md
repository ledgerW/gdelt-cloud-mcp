# GDELT Cloud MCP Server

Model Context Protocol server providing AI agents with secure access to GDELT event data via the GDELT Cloud platform. Query global events, news coverage, and themes through ClickHouse with dual authentication support.

## Features 🚀

- **🔐 Dual Authentication**: OAuth 2.1 with Dynamic Client Registration OR API keys
- **📊 Complete CAMEO Taxonomy**: Country codes, event codes, actor types, and more
- **⚡ ClickHouse Performance**: Fast queries via GDELT Cloud's optimized API
- **🎯 Code Catalog Tools**: Get ALL codes for agents to construct precise queries
- **🔍 Query Tools**: Direct access to Events and GKG tables
- **📚 Comprehensive Resources**: Schema docs, query patterns, best practices

## Quick Start

### Prerequisites

- Python 3.11+
- `uv` package manager ([install](https://github.com/astral-sh/uv))
- GDELT Cloud account with Pro plan ($29/month) or admin access

### Installation

```bash
cd gdelt-cloud-mcp
uv sync
```

### Environment Setup

Create a `.env` file (copy from `.env.example`):

```bash
# GDELT Cloud API
GDELT_CLOUD_API_URL=https://gdeltcloud.com
GDELT_API_KEY=gdelt_sk_your_api_key_here  # Optional: For development testing

# Supabase OAuth (for production OAuth flow)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_anon_key  # Optional
```

### Running the Server

```bash
# Development with FastMCP CLI
uv run fastmcp dev server.py

# Production
uv run fastmcp run server.py

# Or directly
uv run python server.py
```

## Authentication

GDELT Cloud MCP supports two authentication methods:

### 1. OAuth 2.1 (Interactive Users)

**Best for:** ChatGPT, Claude Desktop, human users

**How it works:**
- First connection opens browser for login/consent
- Tokens automatically refresh
- No credentials to manage

**Client Configuration:**

**Claude Desktop** (`~/Library/Application Support/Claude/claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "gdelt-cloud": {
      "url": "https://mcp.gdeltcloud.com",
      "auth": "oauth"
    }
  }
}
```

**Python with FastMCP**:
```python
from fastmcp import Client
from fastmcp.client.auth import OAuth

oauth = OAuth(mcp_url="https://mcp.gdeltcloud.com")

async with Client(
    "https://mcp.gdeltcloud.com",
    auth=oauth
) as client:
    # First use opens browser for consent
    result = await client.call_tool("get_country_codes", {})
```

### 2. API Keys (Developers & Agents)

**Best for:** Automated agents, background jobs, CI/CD

**Generate API Key:**
1. Login to [GDELT Cloud Dashboard](https://gdeltcloud.com/dashboard)
2. Navigate to API Keys
3. Click "Create New Key"
4. Save the key (shown only once!)

**Format:** `gdelt_sk_<64-hex-characters>`

**Python with FastMCP**:
```python
from fastmcp import Client
from fastmcp.client.auth import BearerAuth
import os

async with Client(
    "https://mcp.gdeltcloud.com",
    auth=BearerAuth(token=os.environ["GDELT_API_KEY"])
) as client:
    result = await client.call_tool("query_gdelt_events", {
        "where_clause": "day >= '2025-01-01' AND event_code = '14'",
        "limit": 100
    })
```

## MCP Resources

Static reference documentation accessible via MCP resource URIs:

### CAMEO Taxonomy
- `gdelt://cameo/countries` - ISO 3166-1 alpha-3 country codes
- `gdelt://cameo/actor-types` - Actor type classifications (GOV, MIL, COP, etc.)
- `gdelt://cameo/known-groups` - International organizations (UN, NATO, EU, etc.)
- `gdelt://cameo/ethnic-codes` - Ethnic group classifications
- `gdelt://cameo/religion-codes` - Religious affiliation codes
- `gdelt://cameo/event-codes` - Complete CAMEO event code taxonomy (300+ codes)

### Analysis References
- `gdelt://reference/goldstein-scale` - Event cooperation/conflict intensity mapping
- `gdelt://reference/gkg-themes` - GKG theme taxonomy for semantic analysis
- `gdelt://reference/query-patterns` - Common SQL query patterns
- `gdelt://reference/best-practices` - SQL query best practices
- `gdelt://reference/common-mistakes` - Common query mistakes to avoid

**Access resources:**
```python
# With MCP client
resource = await client.read_resource("gdelt://cameo/event-codes")
print(resource)
```

## MCP Tools

### Code Catalog Tools

These tools return **ALL** codes so agents can find the right ones for their queries.

#### `get_country_codes()`
Returns complete catalog of ISO 3166-1 alpha-3 country codes.

**Usage in queries:**
```sql
actor1_country_code = 'USA'
actor2_country_code IN ('CHN', 'RUS', 'IND')
action_geo_country_code = 'GBR'
```

#### `get_event_codes(category?)`
Returns ALL CAMEO event codes (300+), optionally filtered by category.

**Parameters:**
- `category` (optional): `"verbal_cooperation"`, `"material_cooperation"`, `"verbal_conflict"`, or `"material_conflict"`

**Returns:** Event codes with descriptions, categories, Goldstein scores

**Usage in queries:**
```sql
event_code = '14'  -- Protests
event_root_code = '19'  -- All military force events
event_base_code = '190'  -- Use military force
```

#### `get_actor_type_codes()`
Returns ALL CAMEO actor type codes (GOV, MIL, REB, etc.).

**Usage in queries:**
```sql
actor1_type1_code = 'GOV'  -- Government
actor2_type1_code IN ('MIL', 'REB')  -- Military or Rebels
```

#### `get_known_group_codes()`
Returns ALL known group codes (UN, NATO, EU, etc.).

**Usage in queries:**
```sql
actor1_known_group_code = 'UNO'  -- United Nations
actor2_known_group_code IN ('NATO', 'EU')
```

#### `get_ethnic_codes()`
Returns ALL ethnic group classification codes.

**Usage in queries:**
```sql
actor1_ethnic_code = 'ARB'  -- Arab
actor2_ethnic_code IN ('HIN', 'MUS')
```

#### `get_religion_codes()`
Returns ALL religious affiliation codes.

**Usage in queries:**
```sql
actor1_religion1_code = 'CHR'  -- Christian
actor2_religion1_code IN ('ISL', 'JUD')  -- Muslim or Jewish
```

#### `get_goldstein_scale_mapping()`
Returns complete Goldstein scale mapping for ALL event codes.

**Scale:** -10 (most conflictual) to +10 (most cooperative)

**Usage in queries:**
```sql
goldstein_scale > 5  -- Cooperative events
goldstein_scale < -5  -- Conflictual events
goldstein_scale BETWEEN -2 AND 2  -- Neutral events
```

#### `get_gkg_themes(category?)`
Returns ALL GKG theme codes, optionally filtered by category.

**Categories:** `conflict`, `economy`, `environment`, `health`, `human_rights`, `politics`, `society`, `technology`

**Usage in queries:**
```sql
v1_themes LIKE '%ECON_BANKRUPTCY%'
v2_themes LIKE '%ENV_CLIMATECHANGE%'
(v1_themes LIKE '%LEADER%' OR v2_themes LIKE '%LEADER%')
```

### Query Tools

#### `query_gdelt_events(where_clause, select_fields, limit, order_by)`
Query GDELT events table for structured event data.

**Parameters:**
- `where_clause`: SQL WHERE clause (without WHERE keyword)
- `select_fields`: Comma-separated field names
- `limit`: Maximum rows (1-1000)
- `order_by`: ORDER BY clause (without ORDER BY keyword)

**⚠️ IMPORTANT:** Always include date filter: `day >= 'YYYY-MM-DD'`

**Example:**
```python
result = await client.call_tool("query_gdelt_events", {
    "where_clause": "day >= '2025-01-01' AND event_code = '14' AND action_geo_country_code = 'USA'",
    "select_fields": "global_event_id, day, actor1_name, actor2_name, event_code, goldstein_scale",
    "limit": 100,
    "order_by": "day DESC"
})
```

**Use for:**
- Global events and actor relationships
- Specific event types (protests, conflicts, cooperation)
- Events by country or region
- Bilateral relations analysis
- Event sentiment and impact

#### `query_gdelt_gkg(where_clause, select_fields, limit, order_by)`
Query GDELT GKG (Global Knowledge Graph) for semantic content analysis.

**Parameters:**
- `where_clause`: SQL WHERE clause (without WHERE keyword)
- `select_fields`: Comma-separated field names
- `limit`: Maximum rows (1-1000)
- `order_by`: ORDER BY clause (without ORDER BY keyword)

**⚠️ IMPORTANT:** Always include date filter: `date >= toDateTime('YYYY-MM-DD HH:MM:SS')`

**Example:**
```python
result = await client.call_tool("query_gdelt_gkg", {
    "where_clause": "date >= toDateTime('2025-01-01 00:00:00') AND (v1_themes LIKE '%ECON%' OR v2_themes LIKE '%ECON%')",
    "select_fields": "gkg_record_id, date, source_common_name, v2_themes, v1_5_tone",
    "limit": 100
})
```

**Use for:**
- News article themes and topics
- Sentiment and tone analysis
- Named entities (persons, organizations, locations)
- Media source coverage patterns
- Geographic mentions

## Usage Examples

### Example 1: Find Recent Protests in US

```python
from fastmcp import Client
from fastmcp.client.auth import BearerAuth
import os

async def analyze_us_protests():
    async with Client(
        "https://mcp.gdeltcloud.com",
        auth=BearerAuth(token=os.environ["GDELT_API_KEY"])
    ) as client:
        # First, get the event code for protests
        event_codes = await client.call_tool("get_event_codes", {
            "category": "material_conflict"
        })
        
        # Find protest code (14)
        protest_codes = [
            code for code in event_codes["codes"] 
            if "protest" in code["description"].lower()
        ]
        print(f"Protest codes: {protest_codes}")
        
        # Query US protests
        result = await client.call_tool("query_gdelt_events", {
            "where_clause": "day >= '2025-01-01' AND event_root_code = '14' AND action_geo_country_code = 'USA'",
            "select_fields": "day, actor1_name, event_code, goldstein_scale, num_mentions, avg_tone",
            "limit": 50,
            "order_by": "day DESC"
        })
        
        print(f"Found {result['count']} protests")
        return result["data"]
```

### Example 2: Track Bilateral Relations

```python
async def analyze_us_china_relations():
    async with Client(...) as client:
        # Get country codes
        countries = await client.call_tool("get_country_codes", {})
        usa = "USA"
        chn = "CHN"
        
        # Query interactions
        result = await client.call_tool("query_gdelt_events", {
            "where_clause": f"""
                day >= '2025-01-01' AND
                (
                    (actor1_country_code = '{usa}' AND actor2_country_code = '{chn}') OR
                    (actor1_country_code = '{chn}' AND actor2_country_code = '{usa}')
                )
            """,
            "select_fields": "day, actor1_name, actor2_name, event_code, goldstein_scale, quad_class",
            "limit": 100
        })
        
        return result["data"]
```

### Example 3: Analyze Climate Change News Coverage

```python
async def analyze_climate_news():
    async with Client(...) as client:
        # Get climate-related themes
        themes = await client.call_tool("get_gkg_themes", {
            "category": "environment"
        })
        
        print(f"Environment themes: {themes['themes']}")
        
        # Query GKG for climate change articles
        result = await client.call_tool("query_gdelt_gkg", {
            "where_clause": """
                date >= toDateTime('2025-01-01 00:00:00') AND
                (v1_themes LIKE '%ENV_CLIMATECHANGE%' OR v2_themes LIKE '%ENV_CLIMATECHANGE%')
            """,
            "select_fields": "date, source_common_name, document_identifier, v2_themes, v1_5_tone",
            "limit": 100,
            "order_by": "date DESC"
        })
        
        return result["data"]
```

### Example 4: LangChain Agent Integration

```python
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
import httpx

async def create_gdelt_agent():
    # Initialize MCP client with API key auth
    client = MultiServerMCPClient({
        "gdelt-cloud": {
            "transport": "streamable_http",
            "url": "https://mcp.gdeltcloud.com",
            "auth": httpx.BasicAuth(username="", password=os.environ["GDELT_API_KEY"]),
        }
    })
    
    # Get resources for context
    best_practices = await client.get_resources(
        "gdelt-cloud",
        uris="gdelt://reference/best-practices"
    )
    
    # Get tools
    tools = await client.get_tools(server_name="gdelt-cloud")
    
    # Create agent
    system_prompt = f"""You are a GDELT data analysis assistant.

BEST PRACTICES:
{best_practices[0].as_string()}

AVAILABLE TOOLS:
- Code Catalog Tools: get_country_codes, get_event_codes, get_actor_type_codes, etc.
- Query Tools: query_gdelt_events, query_gdelt_gkg

WORKFLOW:
1. Use code catalog tools to find the right codes for the query
2. Construct precise WHERE clauses using the codes
3. Always include date filters in queries
4. Query events table first (smaller), then GKG if needed"""
    
    agent = create_agent(
        "openai:gpt-4-turbo",
        tools,
        system_prompt=system_prompt
    )
    
    return agent

# Use the agent
agent = await create_gdelt_agent()
result = await agent.ainvoke({
    "messages": "Find all protests in France during January 2025 and analyze their sentiment"
})
```

## GDELT Tables

| Table | Update Frequency | Best For |
|-------|------------------|----------|
| **Events** | 15 minutes | Event tracking, actor analysis, bilateral relations |
| **GKG** | 15 minutes | Themes, entities, sentiment, media coverage |

**Query Priority:** Start with Events (smaller), then GKG if needed

## Best Practices

1. ✅ **Always use date filters** - Required for query performance
2. ✅ **Use code catalog tools first** - Get the right codes before querying
3. ✅ **Select specific fields** - Don't use `SELECT *`
4. ✅ **Start with Events table** - Smaller and faster than GKG
5. ✅ **Check Goldstein scale** - Understand event intensity/sentiment
6. ✅ **Limit results appropriately** - Start with smaller limits

## Common Query Patterns

### Events by Country
```sql
WHERE day >= '2025-01-01' AND action_geo_country_code = 'USA'
```

### Events by Type
```sql
WHERE day >= '2025-01-01' AND event_root_code = '14'  -- Protests
```

### Bilateral Relations
```sql
WHERE day >= '2025-01-01' 
  AND actor1_country_code = 'USA' 
  AND actor2_country_code = 'CHN'
```

### Conflict Events
```sql
WHERE day >= '2025-01-01' AND goldstein_scale < -5
```

### GKG Themes
```sql
WHERE date >= toDateTime('2025-01-01 00:00:00')
  AND (v1_themes LIKE '%ECON%' OR v2_themes LIKE '%ECON%')
```

## Rate Limits

- **API Calls**: 100,000 per month (Pro plan)
- **Request Rate**: 100 requests per minute
- **Concurrent Connections**: 10 simultaneous MCP connections

## Troubleshooting

### Authentication Issues

**"Invalid API key"**
- Verify key format: `gdelt_sk_<64-hex-characters>`
- Check key hasn't been revoked in dashboard
- Ensure Pro plan is active

**OAuth discovery failed**
- Verify Supabase URL is correct
- Check OAuth server is enabled
- Ensure Dynamic Client Registration is enabled

### Query Issues

**"Authentication required"**
- Provide either OAuth token or API key
- Check token hasn't expired (OAuth)
- Verify API key is valid

**Slow queries**
- Add date filters to enable partition pruning
- Select fewer fields
- Reduce limit or date range

**No results**
- Check your WHERE clause syntax
- Verify country/event codes are correct
- Ensure date format is correct

## Resources

- [GDELT Cloud Dashboard](https://gdeltcloud.com/dashboard)
- [GDELT Project Documentation](https://www.gdeltproject.org/)
- [CAMEO Event Codes](https://www.gdeltproject.org/data/lookups/CAMEO.eventcodes.txt)
- [FastMCP Documentation](https://gofastmcp.com/)
- [MCP Specification](https://modelcontextprotocol.io/)

## Support

- **Documentation**: https://docs.gdeltcloud.com
- **Dashboard**: https://gdeltcloud.com/dashboard
- **Email**: support@gdeltcloud.com

## License

This MCP server implementation is provided as-is. GDELT data is freely available for research and analysis.
