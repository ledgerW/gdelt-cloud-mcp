"""
GDELT Cloud MCP Server
Provides access to GDELT event data via ClickHouse with dual authentication support.

Authentication:
- OAuth 2.1 with Dynamic Client Registration (for interactive users)
- API Keys (for developers and automated agents)

Documentation: https://docs.gdeltcloud.com
"""

import os
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv
from fastmcp import FastMCP
from pydantic import Field

# Load environment variables
load_dotenv()

# Import utilities and resources
from utils import GDELTCloudAPIClient, AuthContext, get_auth_token
from cameo import (
    get_country_name,
    search_countries,
    get_quick_reference as get_country_reference,
    get_actor_type,
    search_actor_types,
    get_quick_reference as get_actor_type_reference,
    get_known_group,
    search_known_groups,
    get_quick_reference as get_known_group_reference,
    get_ethnic_code,
    search_ethnic_codes,
    get_quick_reference as get_ethnic_reference,
    get_religion_code,
    search_religions,
    get_quick_reference as get_religion_reference,
    get_event_code,
    search_event_codes,
    get_codes_by_category,
    get_quick_reference as get_event_code_reference,
)
from resources import (
    get_goldstein_score,
    get_goldstein_interpretation,
    get_events_by_intensity,
    get_goldstein_reference,
    search_themes,
    get_themes_by_category,
    get_gkg_themes_reference,
    get_query_pattern,
    get_query_patterns_reference,
    BEST_PRACTICES,
    COMMON_MISTAKES,
)

# Initialize FastMCP server
mcp = FastMCP("GDELT Cloud")

# Global API client (will be initialized with auth context per request)
_api_client: Optional[GDELTCloudAPIClient] = None


async def get_api_client(auth_token: Optional[str] = None) -> GDELTCloudAPIClient:
    """Get or create API client with authentication."""
    token = auth_token or get_auth_token()
    
    if not token:
        raise ValueError("Authentication required. Provide OAuth token or API key.")
    
    base_url = os.getenv('GDELT_CLOUD_API_URL', 'https://gdeltcloud.com')
    return GDELTCloudAPIClient(base_url=base_url, auth_token=token)


# ============================================================================
# CAMEO RESOURCES
# ============================================================================

@mcp.resource("gdelt://cameo/countries")
def get_country_codes_resource() -> str:
    """ISO 3166-1 alpha-3 country codes reference."""
    return get_country_reference()


@mcp.resource("gdelt://cameo/actor-types")
def get_actor_types_resource() -> str:
    """CAMEO actor type classification codes (GOV, MIL, COP, etc.)."""
    return get_actor_type_reference()


@mcp.resource("gdelt://cameo/known-groups")
def get_known_groups_resource() -> str:
    """International organizations and known groups taxonomy."""
    return get_known_group_reference()


@mcp.resource("gdelt://cameo/ethnic-codes")
def get_ethnic_codes_resource() -> str:
    """Ethnic group classification codes."""
    return get_ethnic_reference()


@mcp.resource("gdelt://cameo/religion-codes")
def get_religion_codes_resource() -> str:
    """Religious affiliation classification codes."""
    return get_religion_reference()


@mcp.resource("gdelt://cameo/event-codes")
def get_event_codes_resource() -> str:
    """Complete CAMEO event code taxonomy (300+ codes)."""
    return get_event_code_reference()


@mcp.resource("gdelt://reference/goldstein-scale")
def get_goldstein_scale_resource() -> str:
    """Goldstein scale mapping (event cooperation/conflict intensity)."""
    return get_goldstein_reference()


@mcp.resource("gdelt://reference/gkg-themes")
def get_gkg_themes_resource() -> str:
    """GKG theme taxonomy for semantic analysis."""
    return get_gkg_themes_reference()


@mcp.resource("gdelt://reference/query-patterns")
def get_query_patterns_resource() -> str:
    """Common SQL query patterns and best practices."""
    return get_query_patterns_reference()


@mcp.resource("gdelt://reference/best-practices")
def get_best_practices_resource() -> str:
    """SQL query best practices for GDELT data."""
    return BEST_PRACTICES


@mcp.resource("gdelt://reference/common-mistakes")
def get_common_mistakes_resource() -> str:
    """Common query mistakes to avoid."""
    return COMMON_MISTAKES


# ============================================================================
# CODE CATALOG TOOLS
# ============================================================================

@mcp.tool(tags=["cameo", "reference", "codes"])
def get_country_codes() -> Dict[str, Any]:
    """
    Get ALL ISO 3166-1 alpha-3 country codes.
    
    Returns complete catalog of country codes for use in GDELT queries.
    Use these codes in WHERE clauses like:
    - actor1_country_code = 'USA'
    - actor2_country_code IN ('CHN', 'RUS', 'IND')
    - action_geo_country_code = 'GBR'
    
    Returns:
        Dictionary with all country codes and names
    """
    from cameo.country_codes import load_country_codes
    
    countries = load_country_codes()
    return {
        "codes": [{"code": code, "name": name} for code, name in countries.items()],
        "count": len(countries),
        "usage": "Use in queries: actor1_country_code = 'USA' or action_geo_country_code IN ('CHN', 'RUS')"
    }


@mcp.tool(tags=["cameo", "reference", "codes"])
def get_event_codes(
    category: Optional[str] = Field(None, description="Filter by category: 'verbal_cooperation', 'material_cooperation', 'verbal_conflict', 'material_conflict', or leave empty for all")
) -> Dict[str, Any]:
    """
    Get ALL CAMEO event codes, optionally filtered by category.
    
    Returns complete catalog of event codes (300+ codes) for use in GDELT queries.
    Use these codes in WHERE clauses like:
    - event_code = '14' (Protests)
    - event_root_code = '19' (All level-19 events)
    - event_base_code = '190' (Use military force)
    
    Categories:
    - verbal_cooperation: Diplomatic statements, appeals, requests
    - material_cooperation: Aid, agreements, support
    - verbal_conflict: Threats, accusations, demands
    - material_conflict: Protests, sanctions, military force
    
    Returns:
        Dictionary with event codes, descriptions, categories, and Goldstein scores
    """
    if category:
        events = get_codes_by_category(category)
    else:
        # Get all event codes
        from cameo.event_codes import EVENT_CODES
        events = list(EVENT_CODES.values())
    
    results = []
    for event in events:
        score = get_goldstein_score(event.code)
        results.append({
            "code": event.code,
            "description": event.description,
            "category": event.category,
            "level": event.level,
            "goldstein_score": score,
            "interpretation": get_goldstein_interpretation(score) if score else None
        })
    
    return {
        "codes": results,
        "count": len(results),
        "categories": ["verbal_cooperation", "material_cooperation", "verbal_conflict", "material_conflict"],
        "usage": "Use in queries: event_code = '14' or event_root_code = '19' or event_base_code = '190'"
    }


@mcp.tool(tags=["cameo", "reference", "codes"])
def get_actor_type_codes() -> Dict[str, Any]:
    """
    Get ALL CAMEO actor type classification codes.
    
    Returns complete catalog of actor types (GOV, MIL, COP, etc.) for use in GDELT queries.
    Use these codes in WHERE clauses like:
    - actor1_type1_code = 'GOV' (Government)
    - actor2_type1_code = 'MIL' (Military)
    - actor1_type2_code = 'COP' (Police)
    
    Major types: GOV (Government), MIL (Military), REB (Rebels), OPP (Opposition),
                 PTY (Political Party), COP (Police), JUD (Judiciary), SPY (Intelligence),
                 MED (Media), EDU (Education), BUS (Business), CRM (Criminal), CVL (Civilian)
    
    Returns:
        Dictionary with all actor type codes and descriptions
    """
    from cameo.actor_types import load_actor_types
    
    actor_types = load_actor_types()
    return {
        "codes": [{"code": code, "description": desc} for code, desc in actor_types.items()],
        "count": len(actor_types),
        "usage": "Use in queries: actor1_type1_code = 'GOV' or actor2_type1_code IN ('MIL', 'REB')"
    }


@mcp.tool(tags=["cameo", "reference", "codes"])
def get_known_group_codes() -> Dict[str, Any]:
    """
    Get ALL CAMEO known group codes for international organizations.
    
    Returns complete catalog of known groups (UN, NATO, EU, etc.) for use in GDELT queries.
    Use these codes in WHERE clauses like:
    - actor1_known_group_code = 'UNO' (United Nations)
    - actor2_known_group_code = 'NATO'
    - actor1_known_group_code IN ('IMF', 'WBK') (IMF or World Bank)
    
    Major groups: UNO (UN), NATO, EU, OPEC, WTO, IMF, WBK (World Bank), etc.
    
    Returns:
        Dictionary with all known group codes and names
    """
    from cameo.known_groups import load_known_groups
    
    groups = load_known_groups()
    return {
        "codes": [{"code": code, "name": name} for code, name in groups.items()],
        "count": len(groups),
        "usage": "Use in queries: actor1_known_group_code = 'UNO' or actor2_known_group_code IN ('NATO', 'EU')"
    }


@mcp.tool(tags=["cameo", "reference", "codes"])
def get_ethnic_codes() -> Dict[str, Any]:
    """
    Get ALL CAMEO ethnic group classification codes.
    
    Returns complete catalog of ethnic codes for use in GDELT queries.
    Use these codes in WHERE clauses like:
    - actor1_ethnic_code = 'ARB' (Arab)
    - actor2_ethnic_code = 'HIN' (Hindu)
    
    Returns:
        Dictionary with all ethnic codes and descriptions
    """
    from cameo.ethnic_codes import load_ethnic_codes
    
    ethnic_codes = load_ethnic_codes()
    return {
        "codes": [{"code": code, "description": desc} for code, desc in ethnic_codes.items()],
        "count": len(ethnic_codes),
        "usage": "Use in queries: actor1_ethnic_code = 'ARB' or actor2_ethnic_code IN ('HIN', 'MUS')"
    }


@mcp.tool(tags=["cameo", "reference", "codes"])
def get_religion_codes() -> Dict[str, Any]:
    """
    Get ALL CAMEO religious affiliation classification codes.
    
    Returns complete catalog of religion codes for use in GDELT queries.
    Use these codes in WHERE clauses like:
    - actor1_religion1_code = 'CHR' (Christian)
    - actor2_religion1_code = 'ISL' (Muslim/Islam)
    
    Major religions: CHR (Christian), ISL (Muslim), JUD (Jewish), BUD (Buddhist),
                     HIN (Hindu), SHN (Shinto), etc.
    
    Returns:
        Dictionary with all religion codes and descriptions
    """
    from cameo.religion_codes import load_religion_codes
    
    religion_codes = load_religion_codes()
    return {
        "codes": [{"code": code, "description": desc} for code, desc in religion_codes.items()],
        "count": len(religion_codes),
        "usage": "Use in queries: actor1_religion1_code = 'CHR' or actor2_religion1_code IN ('ISL', 'JUD')"
    }


@mcp.tool(tags=["reference", "goldstein"])
def get_goldstein_scale_mapping() -> Dict[str, Any]:
    """
    Get complete Goldstein scale mapping for ALL event codes.
    
    The Goldstein scale measures event cooperation/conflict intensity from -10 (most conflictual) to +10 (most cooperative).
    
    Returns ALL event codes with their Goldstein scores for use in queries like:
    - WHERE goldstein_scale > 5 (cooperative events)
    - WHERE goldstein_scale < -5 (conflictual events)
    - WHERE goldstein_scale BETWEEN -2 AND 2 (neutral events)
    
    Interpretation:
    - +10 to +8: Highly cooperative (major agreements, peace treaties)
    - +7 to +4: Cooperative (diplomatic cooperation, aid)
    - +3 to -3: Neutral (requests, comments, statements)
    - -4 to -7: Conflictual (threats, protests, sanctions)
    - -8 to -10: Highly conflictual (military force, war)
    
    Returns:
        Dictionary with all event codes and their Goldstein scores
    """
    from resources.goldstein_scale import GOLDSTEIN_SCALE
    
    results = []
    for event_code, score in GOLDSTEIN_SCALE.items():
        event = get_event_code(event_code)
        results.append({
            "event_code": event_code,
            "goldstein_score": score,
            "description": event.description if event else "Unknown",
            "interpretation": get_goldstein_interpretation(score)
        })
    
    return {
        "mappings": results,
        "count": len(results),
        "scale_range": {"min": -10, "max": 10},
        "usage": "Use in queries: goldstein_scale > 5 or goldstein_scale BETWEEN -2 AND 2"
    }


@mcp.tool(tags=["reference", "gkg", "themes"])
def get_gkg_themes(
    category: Optional[str] = Field(None, description="Filter by category: 'conflict', 'economy', 'environment', 'health', 'human_rights', 'politics', 'society', 'technology', or leave empty for all")
) -> Dict[str, Any]:
    """
    Get ALL GKG theme codes, optionally filtered by category.
    
    Returns complete catalog of GKG themes for semantic content analysis.
    Use these themes in WHERE clauses with LIKE operator:
    - v1_themes LIKE '%ECON_BANKRUPTCY%'
    - v2_themes LIKE '%LEADER%'
    - (v1_themes LIKE '%ENV_CLIMATECHANGE%' OR v2_themes LIKE '%ENV_CLIMATECHANGE%')
    
    Categories available: conflict, economy, environment, health, human_rights, politics, society, technology
    
    Note: Always use LIKE with wildcards (%) since themes are stored as concatenated strings.
    
    Returns:
        Dictionary with theme codes organized by category
    """
    if category:
        themes = get_themes_by_category(category)
        return {
            "category": category,
            "themes": themes,
            "count": len(themes),
            "usage": f"Use in queries: v1_themes LIKE '%{themes[0]}%' or v2_themes LIKE '%{themes[0]}%'"
        }
    else:
        # Get all themes by category
        all_themes = {}
        categories = ['conflict', 'economy', 'environment', 'health', 'human_rights', 'politics', 'society', 'technology']
        
        for cat in categories:
            themes = get_themes_by_category(cat)
            all_themes[cat] = themes
        
        # Count total themes
        total = sum(len(themes) for themes in all_themes.values())
        
        return {
            "themes_by_category": all_themes,
            "categories": categories,
            "total_themes": total,
            "usage": "Use in queries with LIKE: v1_themes LIKE '%THEME_CODE%' or v2_themes LIKE '%THEME_CODE%'"
        }


# ============================================================================
# QUERY TOOLS
# ============================================================================

@mcp.tool(tags=["query", "events"])
async def query_gdelt_events(
    where_clause: Optional[str] = Field(
        None, 
        description="SQL WHERE clause (without WHERE keyword). MUST include date filter: day >= 'YYYY-MM-DD'"
    ),
    select_fields: str = Field(
        "global_event_id, day, actor1_name, actor2_name, event_code, goldstein_scale, avg_tone, action_geo_country_code",
        description="Comma-separated field names"
    ),
    limit: int = Field(100, description="Maximum rows (1-1000)", ge=1, le=1000),
    order_by: Optional[str] = Field(None, description="ORDER BY clause (without ORDER BY keyword)")
) -> Dict[str, Any]:
    """
    Query GDELT events table for structured event data.
    
    Use this to analyze:
    - Global events and actor relationships
    - Specific event types (protests, conflicts, cooperation)
    - Events by country or region
    - Bilateral relations between countries
    - Event sentiment and impact
    
    IMPORTANT: Always include date filter for performance!
    Example: where_clause="day >= '2025-01-01' AND event_root_code = '14'"
    
    Returns events with actor information, event classification, and impact metrics.
    """
    try:
        auth_context = AuthContext()
        token = auth_context.require_auth()
        
        async with await get_api_client(token) as client:
            result = await client.query_events(
                where_clause=where_clause,
                select_fields=select_fields,
                limit=limit,
                order_by=order_by
            )
            
            if result.error:
                return {"error": result.error}
            
            return {
                "data": result.data,
                "count": result.count,
                "execution_time": result.execution_time
            }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool(tags=["query", "gkg"])
async def query_gdelt_gkg(
    where_clause: Optional[str] = Field(
        None,
        description="SQL WHERE clause (without WHERE keyword). MUST include date filter: date >= toDateTime('YYYY-MM-DD HH:MM:SS')"
    ),
    select_fields: str = Field(
        "gkg_record_id, date, source_common_name, document_identifier, v2_themes, v1_5_tone",
        description="Comma-separated field names"
    ),
    limit: int = Field(100, description="Maximum rows (1-1000)", ge=1, le=1000),
    order_by: Optional[str] = Field(None, description="ORDER BY clause (without ORDER BY keyword)")
) -> Dict[str, Any]:
    """
    Query GDELT GKG (Global Knowledge Graph) table for semantic content analysis.
    
    Use this to analyze:
    - News article themes and topics
    - Sentiment and tone analysis
    - Named entities (persons, organizations, locations)
    - Media source coverage patterns
    - Geographic mentions and coordinates
    
    IMPORTANT: 
    - Always include date filter for performance!
    - GKG is larger than events - use specific queries
    - Check both v1_themes and v2_themes with LIKE '%THEME%'
    
    Example: where_clause="date >= toDateTime('2025-01-01') AND (v1_themes LIKE '%ECON%' OR v2_themes LIKE '%ECON%')"
    """
    try:
        auth_context = AuthContext()
        token = auth_context.require_auth()
        
        async with await get_api_client(token) as client:
            result = await client.query_gkg(
                where_clause=where_clause,
                select_fields=select_fields,
                limit=limit,
                order_by=order_by
            )
            
            if result.error:
                return {"error": result.error}
            
            return {
                "data": result.data,
                "count": result.count,
                "execution_time": result.execution_time
            }
    except Exception as e:
        return {"error": str(e)}


# ============================================================================
# Run the server
# ============================================================================

if __name__ == "__main__":
    # Note: Authentication is configured via FastMCP CLI or client configuration
    # OAuth: Automatically discovered via Supabase OAuth server
    # API Key: Provided via Authorization: Bearer header
    mcp.run()
