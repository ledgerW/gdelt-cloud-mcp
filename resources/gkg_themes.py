"""
GKG Themes Reference Module
Common theme codes used in Global Knowledge Graph data
Themes are semicolon-delimited in v1_themes and v2_themes columns
"""

from typing import List, Dict

# Theme categories organized by domain
THEME_CATEGORIES: Dict[str, List[str]] = {
    'ECONOMY': [
        'ECON_BANKRUPTCY',
        'ECON_STOCKMARKET',
        'ECON_CURRENCY',
        'ECON_OILPRICE',
        'ECON_INFLATION',
        'ECON_UNEMPLOYMENT',
        'ECON_GDP',
        'ECON_TRADE',
        'ECON_DEBT',
    ],
    'ENVIRONMENT': [
        'ENV_CLIMATECHANGE',
        'ENV_POLLUTION',
        'ENV_DEFORESTATION',
        'ENV_WILDLIFE',
        'ENV_WATER',
        'ENV_ENERGY',
        'ENV_RENEWABLE',
    ],
    'GOVERNMENT': [
        'GOV_ELECTION',
        'GOV_CORRUPTION',
        'GOV_LEGISLATION',
        'GOV_POLICY',
        'GOV_REFERENDUM',
        'GOV_CENSORSHIP',
    ],
    'CONFLICT': [
        'CONFLICT_CIVIL_WAR',
        'CONFLICT_TERRORISM',
        'CONFLICT_MILITARY',
        'CONFLICT_REFUGEE',
        'CONFLICT_CEASEFIRE',
    ],
    'HEALTH': [
        'HEALTH_PANDEMIC',
        'HEALTH_EPIDEMIC',
        'HEALTH_DISEASE',
        'HEALTH_HEALTHCARE',
        'HEALTH_VACCINATION',
    ],
    'TERROR': [
        'TERROR',
        'TERROR_ATTACK',
        'TERROR_ISIS',
        'TERROR_ALQAEDA',
    ],
    'DISASTER': [
        'DISASTER_EARTHQUAKE',
        'DISASTER_FLOOD',
        'DISASTER_HURRICANE',
        'DISASTER_DROUGHT',
        'DISASTER_WILDFIRE',
    ],
    'HUMAN_RIGHTS': [
        'HUMAN_RIGHTS',
        'HUMAN_RIGHTS_ABUSE',
        'PROTEST',
        'CRACKDOWN',
    ],
    'TECHNOLOGY': [
        'TECH_AI',
        'TECH_CYBER',
        'TECH_INTERNET',
        'TECH_SOCIAL_MEDIA',
    ],
    'WORLD_BANK': [
        'WB_1038_LABOR_POLICY',
        'WB_1065_FINANCIAL_SECTOR',
        'WB_634_ECONOMIC_POLICY',
    ],
    'TAX_THEMES': [
        'TAX_FNCACT',  # Financial actions
        'TAX_ETHNICITY',
        'TAX_WORLDLANGUAGES',
    ],
}


def search_themes(query: str) -> List[str]:
    """Search for themes containing the query string (case-insensitive)."""
    lower_query = query.lower()
    all_themes = [theme for themes in THEME_CATEGORIES.values() for theme in themes]
    return [theme for theme in all_themes if lower_query in theme.lower()]


def get_themes_by_category(category: str) -> List[str]:
    """Get all themes in a specific category."""
    return THEME_CATEGORIES.get(category.upper(), [])


def get_all_categories() -> List[str]:
    """Get list of all theme categories."""
    return list(THEME_CATEGORIES.keys())


def get_quick_reference() -> str:
    """Get quick reference guide for GKG themes."""
    return """
GKG Themes - Quick Reference:

Themes are hierarchical codes found in v1_themes and v2_themes columns.
Format: Semicolon-delimited list (e.g., "ECON_BANKRUPTCY;GOV_CORRUPTION")

Common Theme Prefixes:
- ECON_* : Economic themes (bankruptcy, stockmarket, currency, inflation, trade)
- ENV_* : Environmental themes (climate change, pollution, deforestation, energy)
- GOV_* : Government themes (election, corruption, legislation, policy)
- CONFLICT_* : Conflict themes (civil war, terrorism, military, refugee)
- HEALTH_* : Health themes (pandemic, epidemic, disease, vaccination)
- TERROR_* : Terrorism themes (attacks, ISIS, Al Qaeda)
- DISASTER_* : Natural disaster themes (earthquake, flood, hurricane, wildfire)
- WB_* : World Bank taxonomy themes
- TAX_* : GDELT taxonomy themes

Query Patterns:
- Single theme: WHERE v1_themes LIKE '%ECON_BANKRUPTCY%' OR v2_themes LIKE '%ECON_BANKRUPTCY%'
- Multiple themes: WHERE (v1_themes LIKE '%CLIMATE%' OR v2_themes LIKE '%CLIMATE%' OR v1_themes LIKE '%ENV_%' OR v2_themes LIKE '%ENV_%')
- Theme category search: Use wildcards like '%ECON_%' to match all economic themes
- Always search BOTH v1_themes and v2_themes columns for completeness

Sentiment Analysis (v1_5_tone column):
Format: Comma-delimited values: Tone,Positive,Negative,Polarity,ActivityRef,SelfRef,WordCount
- First value is overall tone (-100 to +100)
- Extract: CAST(splitByChar(',', v1_5_tone)[1] AS Float64) > 0 for positive sentiment
- Positive tone: > 5
- Negative tone: < -5
- Neutral: -5 to 5

Important: 
- Themes are case-sensitive
- Use LIKE with % wildcards for fuzzy matching
- Check both v1 and v2 columns for best coverage
- Empty themes = '' means no themes identified
""".strip()
