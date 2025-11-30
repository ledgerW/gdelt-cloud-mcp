"""CAMEO taxonomy reference modules."""

from .event_codes import (
    EVENT_CODES,
    get_event_code,
    search_event_codes,
    get_codes_by_category,
    get_root_codes,
)
from .country_codes import (
    COUNTRY_CODES,
    REGIONS,
    get_country_name,
    search_countries,
)
from .actor_types import (
    ACTOR_TYPES,
    get_actor_type,
    search_actor_types,
)
from .known_groups import (
    KNOWN_GROUPS,
    get_known_group,
    search_known_groups,
)
from .ethnic_codes import (
    ETHNIC_CODES,
    get_ethnic_code,
    search_ethnic_codes,
)
from .religion_codes import (
    RELIGION_CODES,
    get_religion_code,
    search_religions,
)

__all__ = [
    # Event codes
    "EVENT_CODES",
    "get_event_code",
    "search_event_codes",
    "get_codes_by_category",
    "get_root_codes",
    # Country codes
    "COUNTRY_CODES",
    "REGIONS",
    "get_country_name",
    "search_countries",
    # Actor types
    "ACTOR_TYPES",
    "get_actor_type",
    "search_actor_types",
    # Known groups
    "KNOWN_GROUPS",
    "get_known_group",
    "search_known_groups",
    # Ethnic codes
    "ETHNIC_CODES",
    "get_ethnic_code",
    "search_ethnic_codes",
    # Religion codes
    "RELIGION_CODES",
    "get_religion_code",
    "search_religions",
]
