"""
GDELT Cloud MCP Resources
Exports all reference data modules for use in MCP server
"""

from .goldstein_scale import (
    GOLDSTEIN_SCALE,
    get_goldstein_score,
    is_cooperative_event,
    is_conflict_event,
    get_events_by_intensity,
    get_goldstein_interpretation,
    get_quick_reference as get_goldstein_reference,
)

from .gkg_themes import (
    THEME_CATEGORIES,
    search_themes,
    get_themes_by_category,
    get_all_categories,
    get_quick_reference as get_gkg_themes_reference,
)

from .query_patterns import (
    QUERY_PATTERNS,
    BEST_PRACTICES,
    COMMON_MISTAKES,
    get_query_pattern,
    get_all_pattern_names,
    get_quick_reference as get_query_patterns_reference,
)

__all__ = [
    # Goldstein Scale
    'GOLDSTEIN_SCALE',
    'get_goldstein_score',
    'is_cooperative_event',
    'is_conflict_event',
    'get_events_by_intensity',
    'get_goldstein_interpretation',
    'get_goldstein_reference',
    
    # GKG Themes
    'THEME_CATEGORIES',
    'search_themes',
    'get_themes_by_category',
    'get_all_categories',
    'get_gkg_themes_reference',
    
    # Query Patterns
    'QUERY_PATTERNS',
    'BEST_PRACTICES',
    'COMMON_MISTAKES',
    'get_query_pattern',
    'get_all_pattern_names',
    'get_query_patterns_reference',
]
