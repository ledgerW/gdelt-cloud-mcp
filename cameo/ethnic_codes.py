"""
CAMEO Ethnic Codes
Ethnic group classification codes
"""

import os
from typing import Dict, Optional


def _load_ethnic_codes() -> Dict[str, str]:
    """Load ethnic codes from data file."""
    codes = {}
    data_path = os.path.join(os.path.dirname(__file__), "data", "cameo_ethnic.txt")
    
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
ETHNIC_CODES = _load_ethnic_codes()


def get_ethnic_code(code: str) -> Optional[str]:
    """Get ethnic group name for a code."""
    return ETHNIC_CODES.get(code.lower())


def search_ethnic_codes(query: str) -> Dict[str, str]:
    """Search ethnic codes by name."""
    query_lower = query.lower()
    return {
        code: name
        for code, name in ETHNIC_CODES.items()
        if query_lower in name.lower()
    }


def get_quick_reference() -> str:
    """Get formatted quick reference for ethnic codes."""
    # Sample some key groups
    sample_codes = ['ara', 'kur', 'arm', 'aze', 'che', 'rus', 'chi', 'jpn', 
                   'kor', 'tur', 'per', 'jew', 'hin', 'mus', 'ara']
    
    samples = {k: v for k, v in ETHNIC_CODES.items() if k in sample_codes[:10]}
    
    return f"""
CAMEO Ethnic Codes - Quick Reference

Total Ethnic Groups: {len(ETHNIC_CODES)}

Sample Ethnic Groups:
{chr(10).join(f"  {code}: {name}" for code, name in sorted(samples.items())[:15])}
  ... and {len(ETHNIC_CODES) - 15} more

Format: 3-letter lowercase codes
Usage: actor1_ethnic_code, actor2_ethnic_code

Note: Used to identify ethnic dimensions in conflicts and events
    """.strip()
