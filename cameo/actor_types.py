"""
CAMEO Actor Type Codes
Classification codes for actor types in events
"""

import os
from typing import Dict, Optional


def _load_actor_types() -> Dict[str, str]:
    """Load actor type codes from data file."""
    codes = {}
    data_path = os.path.join(os.path.dirname(__file__), "data", "cameo_type.txt")
    
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
ACTOR_TYPES = _load_actor_types()


def get_actor_type(code: str) -> Optional[str]:
    """Get actor type description for a code."""
    return ACTOR_TYPES.get(code.upper())


def search_actor_types(query: str) -> Dict[str, str]:
    """Search actor types by description."""
    query_lower = query.lower()
    return {
        code: desc
        for code, desc in ACTOR_TYPES.items()
        if query_lower in desc.lower()
    }


def get_quick_reference() -> str:
    """Get formatted quick reference for actor types."""
    state_actors = {k: v for k, v in ACTOR_TYPES.items() if k in 
                   ['COP', 'GOV', 'INS', 'JUD', 'MIL', 'OPP', 'REB', 'SEP', 'SPY', 'UAF']}
    
    non_state = {k: v for k, v in ACTOR_TYPES.items() if k in
                ['AGR', 'BUS', 'CRM', 'CVL', 'DEV', 'EDU', 'ELI', 'ENV', 'HLH', 
                 'HRI', 'LAB', 'LEG', 'MED', 'REF']}
    
    return f"""
CAMEO Actor Type Codes - Quick Reference

State Actors ({len(state_actors)}):
{chr(10).join(f"  {code}: {desc}" for code, desc in sorted(state_actors.items()))}

Non-State Actors ({len(non_state)}):
{chr(10).join(f"  {code}: {desc}" for code, desc in sorted(non_state.items()))}

International/Transnational:
  IGO: Inter-Governmental Organization
  IMG: International Militarized Group
  MNC: Multinational Corporation
  NGM: Non-Governmental Movement
  NGO: Non-Governmental Organization

Usage: actor1_type1_code, actor1_type2_code, actor1_type3_code
       (and corresponding actor2 fields)
    """.strip()
