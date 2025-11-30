"""
CAMEO Known Group Codes
Major organizations, international bodies, and known groups
"""

import os
from typing import Dict, Optional


def _load_known_groups() -> Dict[str, str]:
    """Load known group codes from data file."""
    codes = {}
    data_path = os.path.join(os.path.dirname(__file__), "data", "cameo_knowngroup.txt")
    
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
KNOWN_GROUPS = _load_known_groups()


def get_known_group(code: str) -> Optional[str]:
    """Get known group name for a code."""
    return KNOWN_GROUPS.get(code.upper())


def search_known_groups(query: str) -> Dict[str, str]:
    """Search known groups by name."""
    query_lower = query.lower()
    return {
        code: name
        for code, name in KNOWN_GROUPS.items()
        if query_lower in name.lower()
    }


def get_quick_reference() -> str:
    """Get formatted quick reference for known groups."""
    # Sample key groups
    samples = {
        "UNO": "United Nations",
        "NATO": "North Atlantic Treaty Organization",
        "EEC": "European Union",
        "IMF": "International Monetary Fund",
        "WBK": "World Bank",
        "WTO": "World Trade Organization",
        "OAS": "Organization of American States",
        "OAU": "Organization of African Unity",
        "OIC": "Organization of Islamic Conferences",
        "ALQ": "Al Qaeda",
        "HMS": "Hamas",
        "HEZ": "Hezbullah",
        "IRC": "Red Cross",
        "AMN": "Amnesty International",
    }
    
    return f"""
CAMEO Known Group Codes - Quick Reference

Total Groups: {len(KNOWN_GROUPS)}

Key International Organizations:
{chr(10).join(f"  {code}: {name}" for code, name in samples.items() if code in ['UNO', 'NATO', 'EEC', 'IMF', 'WBK', 'WTO'])}

Regional Organizations:
{chr(10).join(f"  {code}: {name}" for code, name in samples.items() if code in ['OAS', 'OAU', 'OIC'])}

Militant Groups (sample):
{chr(10).join(f"  {code}: {name}" for code, name in samples.items() if code in ['ALQ', 'HMS', 'HEZ'])}

NGOs (sample):
{chr(10).join(f"  {code}: {name}" for code, name in samples.items() if code in ['IRC', 'AMN'])}

Usage: actor1_known_group_code, actor2_known_group_code
    """.strip()
