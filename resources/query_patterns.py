"""
Query Patterns Reference Module
Common SQL query patterns and best practices for GDELT data
"""

from typing import Dict

# Common query patterns with placeholders
QUERY_PATTERNS: Dict[str, str] = {
    'EVENT_BY_TYPE': """
-- Find events of specific type
SELECT global_event_id, day, actor1_name, actor2_name, event_code, goldstein_scale, avg_tone
FROM gdelt_events
WHERE event_root_code = '{EVENT_CODE}'  -- e.g., '14' for protests, '19' for conflict
  AND day >= '{START_DATE}'
ORDER BY day DESC
LIMIT {LIMIT}
    """.strip(),
    
    'EVENT_BY_COUNTRY': """
-- Find events involving specific country
SELECT global_event_id, day, actor1_name, actor2_name, event_code, action_geo_country_code, avg_tone
FROM gdelt_events
WHERE (actor1_country_code = '{COUNTRY_CODE}' 
   OR actor2_country_code = '{COUNTRY_CODE}' 
   OR action_geo_country_code = '{COUNTRY_CODE}')
  AND day >= '{START_DATE}'
ORDER BY day DESC
LIMIT {LIMIT}
    """.strip(),
    
    'BILATERAL_EVENTS': """
-- Find events between two countries
SELECT global_event_id, day, actor1_name, actor2_name, event_code, goldstein_scale, avg_tone
FROM gdelt_events
WHERE ((actor1_country_code = '{COUNTRY1}' AND actor2_country_code = '{COUNTRY2}')
    OR (actor1_country_code = '{COUNTRY2}' AND actor2_country_code = '{COUNTRY1}'))
  AND day >= '{START_DATE}'
ORDER BY day DESC
LIMIT {LIMIT}
    """.strip(),
    
    'CONFLICT_INTENSITY': """
-- Find high-intensity conflict events
SELECT global_event_id, day, actor1_name, actor2_name, event_code, action_geo_country_code, 
       goldstein_scale, avg_tone, num_mentions
FROM gdelt_events
WHERE goldstein_scale < -7.0  -- High conflict intensity
  AND event_root_code IN ('18', '19', '20')  -- Assault, Fight, Mass Violence
  AND day >= '{START_DATE}'
ORDER BY goldstein_scale ASC, num_mentions DESC
LIMIT {LIMIT}
    """.strip(),
    
    'SENTIMENT_ANALYSIS': """
-- Analyze sentiment by country/topic
SELECT action_geo_country_code,
       count() as event_count,
       avg(avg_tone) as average_sentiment,
       avg(goldstein_scale) as average_intensity
FROM gdelt_events
WHERE action_geo_country_code != ''
  AND day >= '{START_DATE}'
GROUP BY action_geo_country_code
HAVING event_count > 10
ORDER BY average_sentiment DESC
LIMIT {LIMIT}
    """.strip(),
    
    'TIME_SERIES': """
-- Time series of events by day
SELECT day,
       count() as event_count,
       avg(goldstein_scale) as avg_intensity,
       avg(avg_tone) as avg_sentiment
FROM gdelt_events
WHERE event_root_code = '{EVENT_CODE}'
  AND action_geo_country_code = '{COUNTRY_CODE}'
  AND day BETWEEN '{START_DATE}' AND '{END_DATE}'
GROUP BY day
ORDER BY day ASC
    """.strip(),
    
    'GKG_BY_THEME': """
-- Find articles by theme
SELECT gkg_record_id, date, source_common_name, document_identifier, v2_themes, v1_5_tone
FROM gdelt_gkg
WHERE (v1_themes LIKE '%{THEME}%' OR v2_themes LIKE '%{THEME}%')
  AND date >= toDateTime('{START_DATE}')
ORDER BY date DESC
LIMIT {LIMIT}
    """.strip(),
    
    'GKG_SENTIMENT_BY_THEME': """
-- Analyze sentiment for specific theme
SELECT 
  toDate(date) as day,
  count() as article_count,
  avg(CAST(splitByChar(',', v1_5_tone)[1] AS Float64)) as avg_tone
FROM gdelt_gkg
WHERE (v1_themes LIKE '%{THEME}%' OR v2_themes LIKE '%{THEME}%')
  AND v1_5_tone != ''
  AND date >= toDateTime('{START_DATE}')
GROUP BY day
ORDER BY day DESC
LIMIT {LIMIT}
    """.strip(),
    
    'GKG_TOP_SOURCES': """
-- Find most active sources for topic
SELECT source_common_name,
       count() as article_count
FROM gdelt_gkg
WHERE (v1_themes LIKE '%{THEME}%' OR v2_themes LIKE '%{THEME}%')
  AND date >= toDateTime('{START_DATE}')
  AND source_common_name != ''
GROUP BY source_common_name
ORDER BY article_count DESC
LIMIT {LIMIT}
    """.strip(),
}


# Best practices documentation
BEST_PRACTICES = """
GDELT SQL Query Best Practices:

1. ALWAYS include LIMIT clause (max 1000)
2. ALWAYS use date filters for performance:
   - Events: WHERE day >= 'YYYY-MM-DD'
   - GKG: WHERE date >= toDateTime('YYYY-MM-DD HH:MM:SS')
3. Use exact column names (case-sensitive, lowercase with underscores)
4. For country codes: Use ISO 3166-1 alpha-3 (3-letter codes)
5. For event codes: Use CAMEO codes (01-20 root, with subcodes)
6. For themes: Check BOTH v1_themes and v2_themes with LIKE '%THEME%'
7. For sentiment: 
   - Events: avg_tone column (-100 to +100)
   - GKG: Extract from v1_5_tone with splitByChar(',', v1_5_tone)[1]
8. Use ORDER BY with date/day DESC for most recent first
9. Filter empty values: WHERE column != '' (not IS NOT NULL)
10. For aggregations: Use GROUP BY with HAVING for filtering
""".strip()


# Common mistakes documentation
COMMON_MISTAKES = """
Common Query Mistakes to Avoid:

❌ WHERE day > '2024-01-01' AND day < '2024-12-31'
✅ WHERE day BETWEEN '2024-01-01' AND '2024-12-31'

❌ WHERE country = 'United States'
✅ WHERE actor1_country_code = 'USA'

❌ WHERE event_type = 'protest'
✅ WHERE event_root_code = '14'

❌ WHERE v1_themes = 'ECON_BANKRUPTCY'
✅ WHERE v1_themes LIKE '%ECON_BANKRUPTCY%' OR v2_themes LIKE '%ECON_BANKRUPTCY%'

❌ SELECT * FROM gdelt_events
✅ SELECT specific columns with LIMIT

❌ WHERE date > '2024-01-01'  -- GKG table
✅ WHERE date > toDateTime('2024-01-01')

❌ WHERE goldstein > 5
✅ WHERE goldstein_scale > 5

❌ ORDER BY date  -- ambiguous
✅ ORDER BY day DESC  -- events table

❌ No LIMIT clause
✅ Always include LIMIT (max 1000)
""".strip()


def get_query_pattern(pattern_name: str) -> str:
    """Get a specific query pattern by name."""
    return QUERY_PATTERNS.get(pattern_name, "Pattern not found")


def get_all_pattern_names() -> list:
    """Get list of all available query pattern names."""
    return list(QUERY_PATTERNS.keys())


def get_quick_reference() -> str:
    """Get quick reference guide for query patterns."""
    return """
Query Patterns - Quick Reference:

Common Patterns:
1. Events by type: Filter by event_root_code or event_base_code
2. Events by country: Check actor1_country_code, actor2_country_code, action_geo_country_code
3. Bilateral events: Match both actor1 and actor2 countries
4. Conflict analysis: Filter by goldstein_scale < 0 and event codes 14-20
5. Cooperation analysis: Filter by goldstein_scale > 0 and event codes 01-08
6. Sentiment trends: Aggregate avg_tone or goldstein_scale over time
7. GKG themes: Use LIKE '%THEME%' on v1_themes and v2_themes
8. GKG sentiment: Extract tone from v1_5_tone column

Key Functions:
- toDate(date): Convert datetime to date
- toDateTime('YYYY-MM-DD'): Parse date string
- splitByChar(',', column)[1]: Extract first value from CSV
- CAST(value AS Float64): Convert to number
- today(): Current date
- INTERVAL X DAY: Date arithmetic

ClickHouse Specifics:
- Use single quotes for strings
- Column names are case-sensitive
- Prefer IN over multiple OR conditions
- Use LIMIT for all queries (max 1000)
""".strip()
