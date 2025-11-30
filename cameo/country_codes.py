"""
CAMEO Country Codes
ISO 3166-1 alpha-3 country codes and regional groupings
"""

import os
from typing import Dict, List, Optional


def _load_country_codes() -> Dict[str, str]:
    """Load country codes from data file."""
    codes = {}
    data_path = os.path.join(os.path.dirname(__file__), "data", "cameo_country.txt")
    
    with open(data_path, "r", encoding="utf-8") as f:
        # Skip header
        next(f)
        for line in f:
            line = line.strip()
            if line and "\t" in line:
                code, label = line.split("\t", 1)
                codes[code] = label
    
    return codes


# Load codes once at module import
COUNTRY_CODES = _load_country_codes()

# Regional groupings (from the data file)
REGIONS = {
    "WSB": "West Bank",
    "BAG": "Baghdad", 
    "GZS": "Gaza Strip",
    "AFR": "Africa",
    "ASA": "Asia",
    "BLK": "Balkans",
    "CRB": "Caribbean",
    "CAU": "Caucasus",
    "CFR": "Central Africa",
    "CAS": "Central Asia",
    "CEU": "Central Europe",
    "EIN": "East Indies",
    "EAF": "Eastern Africa",
    "EEU": "Eastern Europe",
    "EUR": "Europe",
    "LAM": "Latin America",
    "MEA": "Middle East",
    "MDT": "Mediterranean",
    "NAF": "North Africa",
    "NMR": "North America",
    "PGS": "Persian Gulf",
    "SCN": "Scandinavia",
    "SAM": "South America",
    "SAS": "South Asia",
    "SEA": "Southeast Asia",
    "SAF": "Southern Africa",
    "WAF": "West Africa",
    "WST": "The West",
}


def get_country_name(code: str) -> Optional[str]:
    """Get country/region name for a CAMEO country code."""
    return COUNTRY_CODES.get(code.upper())


def search_countries(query: str) -> Dict[str, str]:
    """Search country codes by name."""
    query_lower = query.lower()
    return {
        code: name
        for code, name in COUNTRY_CODES.items()
        if query_lower in name.lower()
    }


def is_region(code: str) -> bool:
    """Check if code represents a region rather than a country."""
    return code.upper() in REGIONS


def get_all_countries() -> Dict[str, str]:
    """Get all country codes (excluding regions)."""
    return {
        code: name
        for code, name in COUNTRY_CODES.items()
        if code not in REGIONS
    }


def get_quick_reference() -> str:
    """Get formatted quick reference for country codes."""
    return f"""
CAMEO Country Codes - Quick Reference

Standard: ISO 3166-1 alpha-3 codes
Format: 3-letter codes (e.g., USA, CHN, RUS, GBR, DEU)
Usage: actor1_country_code, actor2_country_code, action_geo_country_code

Regional Groupings ({len(REGIONS)} regions):
{chr(10).join(f"  {code}: {name}" for code, name in sorted(REGIONS.items())[:10])}
  ... and {len(REGIONS) - 10} more

Countries ({len(get_all_countries())} total):
  Examples: USA (United States), CHN (China), RUS (Russia), 
            GBR (United Kingdom), DEU (Germany), FRA (France),
            JPN (Japan), IND (India), BRA (Brazil), etc.

Tip: Always use 3-letter ISO codes, NOT country names in queries.
    """.strip()
