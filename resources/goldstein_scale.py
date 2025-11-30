"""
Goldstein Scale Reference Module
Maps CAMEO event codes to Goldstein scale values (-10 to +10)
Negative values = conflict, Positive values = cooperation
"""

from typing import Dict, List, Optional

# Goldstein Scale mapping (event_code -> goldstein_value)
GOLDSTEIN_SCALE: Dict[str, float] = {
    # COOPERATION EVENTS (Positive Values)
    '01': 0.0, '010': 0.0, '011': -0.1, '012': -0.4, '013': 0.4, '014': 0.0,
    '015': 0.0, '016': -2.0, '017': 0.0, '018': 3.4, '019': 3.4,
    
    '02': 3.0, '020': 3.0, '021': 3.4, '0211': 3.4, '0212': 3.4, '0213': 3.4,
    '0214': 3.4, '022': 3.2, '023': 3.4, '0231': 3.4, '0232': 3.4, '0233': 3.4,
    '0234': 3.4, '024': -0.3, '0241': -0.3, '0242': -0.3, '0243': -0.3,
    '0244': -0.3, '025': -0.3, '0251': -0.3, '0252': -0.3, '0253': -0.3,
    '0254': -0.3, '0255': -0.3, '0256': -0.3, '026': 4.0, '027': 4.0, '028': 4.0,
    
    '03': 4.0, '030': 4.0, '031': 5.2, '0311': 5.2, '0312': 5.2, '0313': 5.2,
    '0314': 5.2, '032': 4.5, '033': 5.2, '0331': 5.2, '0332': 5.2, '0333': 5.2,
    '0334': 6.0, '034': 7.0, '0341': 7.0, '0342': 7.0, '0343': 7.0, '0344': 7.0,
    '035': 7.0, '0351': 7.0, '0352': 7.0, '0353': 7.0, '0354': 7.0, '0355': 7.0,
    '0356': 7.0, '036': 4.0, '037': 5.0, '038': 7.0, '039': 5.0,
    
    '04': 1.0, '040': 1.0, '041': 1.0, '042': 1.9, '043': 2.8, '044': 2.5,
    '045': 5.0, '046': 7.0,
    
    '05': 3.5, '050': 3.5, '051': 3.4, '052': 3.5, '053': 3.8, '054': 6.0,
    '055': 7.0, '056': 7.0, '057': 8.0,
    
    '06': 6.0, '060': 6.0, '061': 6.4, '062': 7.4, '063': 7.4, '064': 7.0,
    
    '07': 7.0, '070': 7.0, '071': 7.4, '072': 8.3, '073': 7.4, '074': 8.5, '075': 7.0,
    
    '08': 5.0, '080': 5.0, '081': 5.0, '0811': 5.0, '0812': 5.0, '0813': 5.0,
    '0814': 5.0, '082': 5.0, '083': 5.0, '0831': 5.0, '0832': 5.0, '0833': 5.0,
    '0834': 5.0, '084': 7.0, '0841': 7.0, '0842': 7.0, '085': 7.0, '086': 9.0,
    '0861': 9.0, '0862': 9.0, '0863': 9.0, '087': 9.0, '0871': 9.0, '0872': 9.0,
    '0873': 9.0, '0874': 10.0,
    
    # NEUTRAL/MIXED EVENTS
    '09': -2.0, '090': -2.0, '091': -2.0, '092': -2.0, '093': -2.0, '094': -2.0,
    
    '10': -5.0, '100': -5.0, '101': -5.0, '1011': -5.0, '1012': -5.0, '1013': -5.0,
    '1014': -5.0, '102': -5.0, '103': -5.0, '1031': -5.0, '1032': -5.0, '1033': -5.0,
    '1034': -5.0, '104': -5.0, '1041': -5.0, '1042': -5.0, '1043': -5.0, '1044': -5.0,
    '105': -5.0, '1051': -5.0, '1052': -5.0, '1053': -5.0, '1054': -5.0, '1055': -5.0,
    '1056': -5.0, '107': -5.0, '108': -5.0,
    
    # CONFLICT EVENTS (Negative Values)
    '11': -2.0, '110': -2.0, '111': -2.0, '112': -2.0, '1121': -2.0, '1122': -2.0,
    '1123': -2.0, '1124': -2.0, '1125': -2.0, '113': -2.0, '114': -2.0, '115': -2.0,
    '116': -2.0,
    
    '12': -4.0, '120': -4.0, '121': -4.0, '1211': -4.0, '1212': -4.0, '122': -4.0,
    '1221': -4.0, '1222': -4.0, '1223': -4.0, '1224': -4.0, '123': -4.0, '1231': -4.0,
    '1232': -4.0, '1233': -4.0, '1234': -4.0, '124': -4.0, '1241': -4.0, '1242': -4.0,
    '1243': -4.0, '1244': -4.0, '1245': -4.0, '1246': -4.0, '125': -5.0, '126': -5.0,
    '127': -5.0, '128': -5.0, '129': -5.0,
    
    '13': -6.0, '130': -4.4, '131': -5.8, '1311': -5.8, '1312': -5.8, '1313': -5.8,
    '132': -5.8, '1321': -5.8, '1322': -5.8, '1323': -5.8, '1324': -5.8, '133': -5.8,
    '134': -5.8, '135': -5.8, '136': -7.0, '137': -7.0, '138': -7.0, '1381': -7.0,
    '1382': -7.0, '1383': -7.0, '1384': -7.0, '1385': -7.0, '139': -7.0,
    
    '14': -6.5, '140': -6.5, '141': -6.5, '1411': -6.5, '1412': -6.5, '1413': -6.5,
    '1414': -6.5, '142': -6.5, '1421': -6.5, '1422': -6.5, '1423': -6.5, '1424': -6.5,
    '143': -6.5, '1431': -6.5, '1432': -6.5, '1433': -6.5, '1434': -6.5, '144': -7.5,
    '1441': -7.5, '1442': -7.5, '1443': -7.5, '1444': -7.5, '145': -7.5, '1451': -7.5,
    '1452': -7.5, '1453': -7.5, '1454': -7.5,
    
    '15': -7.2, '150': -7.2, '151': -7.2, '152': -7.2, '153': -7.2, '154': -7.2,
    
    '16': -4.0, '160': -4.0, '161': -4.0, '162': -5.6, '1621': -5.6, '1622': -5.6,
    '1623': -5.6, '163': -8.0, '164': -7.0, '165': -6.5, '166': -7.0, '1661': -7.0,
    '1662': -7.0, '1663': -7.0,
    
    '17': -7.0, '170': -7.0, '171': -9.2, '1711': -9.2, '1712': -9.2, '172': -5.0,
    '1721': -5.0, '1722': -5.0, '1723': -5.0, '1724': -5.0, '173': -5.0, '174': -5.0,
    '175': -9.0,
    
    '18': -9.0, '180': -9.0, '181': -9.0, '182': -9.5, '1821': -9.0, '1822': -9.0,
    '1823': -10.0, '183': -10.0, '1831': -10.0, '1832': -10.0, '1833': -10.0,
    '184': -8.0, '185': -8.0, '186': -10.0,
    
    '19': -10.0, '190': -10.0, '191': -9.5, '192': -9.5, '193': -10.0, '194': -10.0,
    '195': -10.0, '196': -9.5,
    
    '20': -10.0, '200': -10.0, '201': -9.5, '202': -10.0, '203': -10.0, '204': -10.0,
    '2041': -10.0, '2042': -10.0,
}


def get_goldstein_score(event_code: str) -> Optional[float]:
    """Get Goldstein scale value for an event code."""
    return GOLDSTEIN_SCALE.get(event_code)


def is_cooperative_event(event_code: str) -> bool:
    """Check if event code represents cooperation (positive Goldstein score)."""
    score = GOLDSTEIN_SCALE.get(event_code)
    return score is not None and score > 0


def is_conflict_event(event_code: str) -> bool:
    """Check if event code represents conflict (negative Goldstein score)."""
    score = GOLDSTEIN_SCALE.get(event_code)
    return score is not None and score < 0


def get_events_by_intensity(min_score: float, max_score: float) -> List[str]:
    """Get all event codes within a Goldstein scale range."""
    return [
        code for code, score in GOLDSTEIN_SCALE.items()
        if min_score <= score <= max_score
    ]


def get_goldstein_interpretation(score: float) -> str:
    """Get human-readable interpretation of a Goldstein scale value."""
    if score >= 8:
        return 'Very Strong Cooperation'
    elif score >= 6:
        return 'Strong Cooperation'
    elif score >= 4:
        return 'Moderate Cooperation'
    elif score >= 2:
        return 'Mild Cooperation'
    elif score > 0:
        return 'Slight Cooperation'
    elif score == 0:
        return 'Neutral'
    elif score > -2:
        return 'Slight Conflict'
    elif score > -4:
        return 'Mild Conflict'
    elif score > -6:
        return 'Moderate Conflict'
    elif score > -8:
        return 'Strong Conflict'
    else:
        return 'Very Strong Conflict'


def get_quick_reference() -> str:
    """Get quick reference guide for Goldstein scale."""
    return """
Goldstein Scale - Quick Reference:

Scale Range: -10 (Most Conflictual) to +10 (Most Cooperative)

COOPERATION (Positive Values):
+10.0 - Military surrender/retreat (0874)
+9.0  - Allow peacekeepers, inspectors, humanitarian aid (086x, 087x)
+8.5  - Provide military protection (074)
+8.3  - Provide military aid (072)
+8.0  - Sign formal agreement (057)
+7.4  - Provide economic/humanitarian aid, cooperate militarily (071, 073, 062, 063)
+7.0  - Major concessions, accept mediation, share intel (034x, 035x, 038, 064, 07x, 084x, 085)
+6.0  - Material cooperation, grant recognition (06, 0334, 054)
+5.0  - Yield, settle disputes (08, 037, 039, 045)
+4.0  - Intent to cooperate, appeals, consultations (03, 026-028, 036)
+3.0  - Appeals for cooperation (02)
+1.0  - Consultations (04)
 0.0  - Neutral statements (01)

CONFLICT (Negative Values):
 -2.0  - Investigate, disapprove, accuse (09, 11)
 -4.0  - Reject requests, refuse to yield (12)
 -5.0  - Demand, impose restrictions (10, 172x, 173, 174)
 -6.0  - Threaten (13 root)
 -6.5  - Protests, strikes (14)
 -7.0  - Threats of force, reduce relations, coerce (136-139, 16, 17)
 -7.5  - Violent protests, obstruct passage (144, 145)
 -8.0  - Impose sanctions, use as shield (163, 184, 185)
 -9.0  - Assault, violent repression (175, 18)
 -9.5  - Military blockade, physical assault (191, 192, 182, 196, 201)
-10.0  - Kill, fight, mass violence (1823, 183x, 186, 19, 20)

Usage Tips:
- Values < -5: Significant conflict
- Values -5 to 0: Tension/neutral
- Values 0 to 5: Mild to moderate cooperation
- Values > 5: Strong cooperation
""".strip()
