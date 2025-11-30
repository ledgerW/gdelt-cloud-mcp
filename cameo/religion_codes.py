"""
CAMEO Religion Codes
Religious affiliation classification codes
"""

import os
from typing import Dict, Optional


def _load_religion_codes() -> Dict[str, str]:
    """Load religion codes from data file."""
    codes = {}
    data_path = os.path.join(os.path.dirname(__file__), "data", "cameo_religion.txt")
    
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
RELIGION_CODES = _load_religion_codes()


def get_religion_code(code: str) -> Optional[str]:
    """Get religion name for a code."""
    return RELIGION_CODES.get(code.upper())


def search_religions(query: str) -> Dict[str, str]:
    """Search religion codes by name."""
    query_lower = query.lower()
    return {
        code: name
        for code, name in RELIGION_CODES.items()
        if query_lower in name.lower()
    }


def get_quick_reference() -> str:
    """Get formatted quick reference for religion codes."""
    major_religions = {
        "CHR": "Christianity",
        "MOS": "Muslim", 
        "HIN": "Hinduism",
        "BUD": "Buddhism",
        "JEW": "Judaism",
        "SIK": "Sikh",
    }
    
    denominations = {
        "CTH": "Catholic",
        "PRO": "Protestant",
        "DOX": "Orthodox",
        "SUN": "Sunni",
        "SHI": "Shia",
        "SFI": "Sufi",
    }
    
    return f"""
CAMEO Religion Codes - Quick Reference

Total Religion Codes: {len(RELIGION_CODES)}

Major Religions:
{chr(10).join(f"  {code}: {name}" for code, name in major_religions.items())}

Denominations/Sects:
{chr(10).join(f"  {code}: {name}" for code, name in denominations.items())}

Other:
  ATH: Agnostic
  BAH: Bahai Faith
  CON: Confucianism
  TAO: Taoist
  ZRO: Zoroastrianism
  JAN: Jainism
  DRZ: Druze

Format: 3-letter uppercase codes
Usage: actor1_religion1_code, actor1_religion2_code
       actor2_religion1_code, actor2_religion2_code

Note: Used to identify religious dimensions in conflicts and events
    """.strip()
