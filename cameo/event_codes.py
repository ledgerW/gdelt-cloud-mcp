"""
CAMEO Event Codes
Complete hierarchy of Conflict and Mediation Event Observations (CAMEO) codes
Adapted from GDELT Project: https://www.gdeltproject.org/data/lookups/CAMEO.eventcodes.txt
"""

from typing import Dict, List, Optional, Literal


CategoryType = Literal["cooperation", "neutral", "conflict"]
LevelType = Literal["root", "base", "leaf"]


class EventCode:
    """CAMEO Event Code with metadata."""
    
    def __init__(
        self,
        code: str,
        description: str,
        category: CategoryType,
        level: LevelType
    ):
        self.code = code
        self.description = description
        self.category = category
        self.level = level
    
    def to_dict(self) -> Dict:
        return {
            "code": self.code,
            "description": self.description,
            "category": self.category,
            "level": self.level
        }


# Complete CAMEO event code taxonomy (300+ codes)
# This mirrors the structure from nextjs_/lib/langchain/gdelt-reference/event-codes.ts
def _build_event_codes() -> Dict[str, EventCode]:
    """Build the complete event codes dictionary."""
    codes = {}
    
    # Helper to add codes
    def add(code: str, desc: str, cat: CategoryType, lvl: LevelType):
        codes[code] = EventCode(code, desc, cat, lvl)
    
    # COOPERATION (01-08)
    add("01", "MAKE PUBLIC STATEMENT", "cooperation", "root")
    add("010", "Make statement, not specified below", "cooperation", "base")
    add("011", "Decline comment", "cooperation", "leaf")
    add("012", "Make pessimistic comment", "cooperation", "leaf")
    add("013", "Make optimistic comment", "cooperation", "leaf")
    add("014", "Consider policy option", "cooperation", "leaf")
    add("015", "Acknowledge or claim responsibility", "cooperation", "leaf")
    add("016", "Deny responsibility", "cooperation", "leaf")
    add("017", "Engage in symbolic act", "cooperation", "leaf")
    add("018", "Make empathetic comment", "cooperation", "leaf")
    add("019", "Express accord", "cooperation", "leaf")
    
    add("02", "APPEAL", "cooperation", "root")
    add("020", "Appeal, not specified below", "cooperation", "base")
    add("021", "Appeal for material cooperation, not specified below", "cooperation", "base")
    add("0211", "Appeal for economic cooperation", "cooperation", "leaf")
    add("0212", "Appeal for military cooperation", "cooperation", "leaf")
    add("0213", "Appeal for judicial cooperation", "cooperation", "leaf")
    add("0214", "Appeal for intelligence", "cooperation", "leaf")
    add("022", "Appeal for diplomatic cooperation, such as policy support", "cooperation", "leaf")
    add("023", "Appeal for aid, not specified below", "cooperation", "base")
    add("0231", "Appeal for economic aid", "cooperation", "leaf")
    add("0232", "Appeal for military aid", "cooperation", "leaf")
    add("0233", "Appeal for humanitarian aid", "cooperation", "leaf")
    add("0234", "Appeal for military protection or peacekeeping", "cooperation", "leaf")
    add("024", "Appeal for political reform, not specified below", "cooperation", "base")
    add("0241", "Appeal for change in leadership", "cooperation", "leaf")
    add("0242", "Appeal for policy change", "cooperation", "leaf")
    add("0243", "Appeal for rights", "cooperation", "leaf")
    add("0244", "Appeal for change in institutions, regime", "cooperation", "leaf")
    add("025", "Appeal to yield", "cooperation", "base")
    add("0251", "Appeal for easing of administrative sanctions", "cooperation", "leaf")
    add("0252", "Appeal for easing of popular dissent", "cooperation", "leaf")
    add("0253", "Appeal for release of persons or property", "cooperation", "leaf")
    add("0254", "Appeal for easing of economic sanctions, boycott, or embargo", "cooperation", "leaf")
    add("0255", "Appeal for target to allow international involvement (non-mediation)", "cooperation", "leaf")
    add("0256", "Appeal for de-escalation of military engagement", "cooperation", "leaf")
    add("026", "Appeal to others to meet or negotiate", "cooperation", "leaf")
    add("027", "Appeal to others to settle dispute", "cooperation", "leaf")
    add("028", "Appeal to others to engage in or accept mediation", "cooperation", "leaf")
    
    add("03", "EXPRESS INTENT TO COOPERATE", "cooperation", "root")
    add("030", "Express intent to cooperate, not specified below", "cooperation", "base")
    add("031", "Express intent to engage in material cooperation, not specified below", "cooperation", "base")
    add("0311", "Express intent to cooperate economically", "cooperation", "leaf")
    add("0312", "Express intent to cooperate militarily", "cooperation", "leaf")
    add("0313", "Express intent to cooperate on judicial matters", "cooperation", "leaf")
    add("0314", "Express intent to cooperate on intelligence", "cooperation", "leaf")
    add("032", "Express intent to provide diplomatic cooperation such as policy support", "cooperation", "leaf")
    add("033", "Express intent to provide material aid, not specified below", "cooperation", "base")
    add("0331", "Express intent to provide economic aid", "cooperation", "leaf")
    add("0332", "Express intent to provide military aid", "cooperation", "leaf")
    add("0333", "Express intent to provide humanitarian aid", "cooperation", "leaf")
    add("0334", "Express intent to provide military protection or peacekeeping", "cooperation", "leaf")
    add("034", "Express intent to institute political reform, not specified below", "cooperation", "base")
    add("0341", "Express intent to change leadership", "cooperation", "leaf")
    add("0342", "Express intent to change policy", "cooperation", "leaf")
    add("0343", "Express intent to provide rights", "cooperation", "leaf")
    add("0344", "Express intent to change institutions, regime", "cooperation", "leaf")
    add("035", "Express intent to yield, not specified below", "cooperation", "base")
    add("0351", "Express intent to ease administrative sanctions", "cooperation", "leaf")
    add("0352", "Express intent to ease popular dissent", "cooperation", "leaf")
    add("0353", "Express intent to release persons or property", "cooperation", "leaf")
    add("0354", "Express intent to ease economic sanctions, boycott, or embargo", "cooperation", "leaf")
    add("0355", "Express intent allow international involvement (not mediation)", "cooperation", "leaf")
    add("0356", "Express intent to de-escalate military engagement", "cooperation", "leaf")
    add("036", "Express intent to meet or negotiate", "cooperation", "leaf")
    add("037", "Express intent to settle dispute", "cooperation", "leaf")
    add("038", "Express intent to accept mediation", "cooperation", "leaf")
    add("039", "Express intent to mediate", "cooperation", "leaf")
    
    add("04", "CONSULT", "cooperation", "root")
    add("040", "Consult, not specified below", "cooperation", "base")
    add("041", "Discuss by telephone", "cooperation", "leaf")
    add("042", "Make a visit", "cooperation", "leaf")
    add("043", "Host a visit", "cooperation", "leaf")
    add("044", "Meet at a third location", "cooperation", "leaf")
    add("045", "Mediate", "cooperation", "leaf")
    add("046", "Engage in negotiation", "cooperation", "leaf")
    
    add("05", "ENGAGE IN DIPLOMATIC COOPERATION", "cooperation", "root")
    add("050", "Engage in diplomatic cooperation, not specified below", "cooperation", "base")
    add("051", "Praise or endorse", "cooperation", "leaf")
    add("052", "Defend verbally", "cooperation", "leaf")
    add("053", "Rally support on behalf of", "cooperation", "leaf")
    add("054", "Grant diplomatic recognition", "cooperation", "leaf")
    add("055", "Apologize", "cooperation", "leaf")
    add("056", "Forgive", "cooperation", "leaf")
    add("057", "Sign formal agreement", "cooperation", "leaf")
    
    add("06", "ENGAGE IN MATERIAL COOPERATION", "cooperation", "root")
    add("060", "Engage in material cooperation, not specified below", "cooperation", "base")
    add("061", "Cooperate economically", "cooperation", "leaf")
    add("062", "Cooperate militarily", "cooperation", "leaf")
    add("063", "Engage in judicial cooperation", "cooperation", "leaf")
    add("064", "Share intelligence or information", "cooperation", "leaf")
    
    add("07", "PROVIDE AID", "cooperation", "root")
    add("070", "Provide aid, not specified below", "cooperation", "base")
    add("071", "Provide economic aid", "cooperation", "leaf")
    add("072", "Provide military aid", "cooperation", "leaf")
    add("073", "Provide humanitarian aid", "cooperation", "leaf")
    add("074", "Provide military protection or peacekeeping", "cooperation", "leaf")
    add("075", "Grant asylum", "cooperation", "leaf")
    
    add("08", "YIELD", "cooperation", "root")
    add("080", "Yield, not specified below", "cooperation", "base")
    add("081", "Ease administrative sanctions, not specified below", "cooperation", "base")
    add("0811", "Ease restrictions on political freedoms", "cooperation", "leaf")
    add("0812", "Ease ban on political parties or politicians", "cooperation", "leaf")
    add("0813", "Ease curfew", "cooperation", "leaf")
    add("0814", "Ease state of emergency or martial law", "cooperation", "leaf")
    add("082", "Ease political dissent", "cooperation", "leaf")
    add("083", "Accede to requests or demands for political reform not specified below", "cooperation", "base")
    add("0831", "Accede to demands for change in leadership", "cooperation", "leaf")
    add("0832", "Accede to demands for change in policy", "cooperation", "leaf")
    add("0833", "Accede to demands for rights", "cooperation", "leaf")
    add("0834", "Accede to demands for change in institutions, regime", "cooperation", "leaf")
    add("084", "Return, release, not specified below", "cooperation", "base")
    add("0841", "Return, release person(s)", "cooperation", "leaf")
    add("0842", "Return, release property", "cooperation", "leaf")
    add("085", "Ease economic sanctions, boycott, embargo", "cooperation", "leaf")
    add("086", "Allow international involvement not specified below", "cooperation", "base")
    add("0861", "Receive deployment of peacekeepers", "cooperation", "leaf")
    add("0862", "Receive inspectors", "cooperation", "leaf")
    add("0863", "Allow delivery of humanitarian aid", "cooperation", "leaf")
    add("087", "De-escalate military engagement", "cooperation", "base")
    add("0871", "Declare truce, ceasefire", "cooperation", "leaf")
    add("0872", "Ease military blockade", "cooperation", "leaf")
    add("0873", "Demobilize armed forces", "cooperation", "leaf")
    add("0874", "Retreat or surrender militarily", "cooperation", "leaf")
    
    # NEUTRAL/MIXED (09-13)
    add("09", "INVESTIGATE", "neutral", "root")
    add("090", "Investigate, not specified below", "neutral", "base")
    add("091", "Investigate crime, corruption", "neutral", "leaf")
    add("092", "Investigate human rights abuses", "neutral", "leaf")
    add("093", "Investigate military action", "neutral", "leaf")
    add("094", "Investigate war crimes", "neutral", "leaf")
    
    add("10", "DEMAND", "neutral", "root")
    add("100", "Demand, not specified below", "neutral", "base")
    add("101", "Demand information, investigation", "neutral", "leaf")
    add("1011", "Demand economic cooperation", "neutral", "leaf")
    add("1012", "Demand military cooperation", "neutral", "leaf")
    add("1013", "Demand judicial cooperation", "neutral", "leaf")
    add("1014", "Demand intelligence cooperation", "neutral", "leaf")
    add("102", "Demand policy support", "neutral", "leaf")
    add("103", "Demand aid, protection, or peacekeeping", "neutral", "base")
    add("1031", "Demand economic aid", "neutral", "leaf")
    add("1032", "Demand military aid", "neutral", "leaf")
    add("1033", "Demand humanitarian aid", "neutral", "leaf")
    add("1034", "Demand military protection or peacekeeping", "neutral", "leaf")
    add("104", "Demand political reform, not specified below", "neutral", "base")
    add("1041", "Demand change in leadership", "neutral", "leaf")
    add("1042", "Demand policy change", "neutral", "leaf")
    add("1043", "Demand rights", "neutral", "leaf")
    add("1044", "Demand change in institutions, regime", "neutral", "leaf")
    add("105", "Demand mediation", "neutral", "leaf")
    add("1051", "Demand easing of administrative sanctions", "neutral", "leaf")
    add("1052", "Demand easing of political dissent", "neutral", "leaf")
    add("1053", "Demand release of persons or property", "neutral", "leaf")
    add("1054", "Demand easing of economic sanctions, boycott, or embargo", "neutral", "leaf")
    add("1055", "Demand that target allows international involvement (non-mediation)", "neutral", "leaf")
    add("1056", "Demand de-escalation of military engagement", "neutral", "leaf")
    add("106", "Demand withdrawal", "neutral", "leaf")
    add("107", "Demand ceasefire", "neutral", "leaf")
    add("108", "Demand meeting, negotiation", "neutral", "leaf")
    
    # CONFLICT (11-20) - Continuing with remaining codes...
    add("11", "DISAPPROVE", "conflict", "root")
    add("110", "Disapprove, not specified below", "conflict", "base")
    add("111", "Criticize or denounce", "conflict", "leaf")
    add("112", "Accuse, not specified below", "conflict", "base")
    add("1121", "Accuse of crime, corruption", "conflict", "leaf")
    add("1122", "Accuse of human rights abuses", "conflict", "leaf")
    add("1123", "Accuse of aggression", "conflict", "leaf")
    add("1124", "Accuse of war crimes", "conflict", "leaf")
    add("1125", "Accuse of espionage, treason", "conflict", "leaf")
    add("113", "Rally opposition against", "conflict", "leaf")
    add("114", "Complain officially", "conflict", "leaf")
    add("115", "Bring lawsuit against", "conflict", "leaf")
    add("116", "Find guilty or liable (legally)", "conflict", "leaf")
    
    add("12", "REJECT", "conflict", "root")
    add("120", "Reject, not specified below", "conflict", "base")
    add("121", "Reject material cooperation", "conflict", "base")
    add("1211", "Reject economic cooperation", "conflict", "leaf")
    add("1212", "Reject military cooperation", "conflict", "leaf")
    add("122", "Reject request or demand for material aid, not specified below", "conflict", "base")
    add("1221", "Reject request for economic aid", "conflict", "leaf")
    add("1222", "Reject request for military aid", "conflict", "leaf")
    add("1223", "Reject request for humanitarian aid", "conflict", "leaf")
    add("1224", "Reject request for military protection or peacekeeping", "conflict", "leaf")
    add("123", "Reject request or demand for political reform, not specified below", "conflict", "base")
    add("1231", "Reject request for change in leadership", "conflict", "leaf")
    add("1232", "Reject request for policy change", "conflict", "leaf")
    add("1233", "Reject request for rights", "conflict", "leaf")
    add("1234", "Reject request for change in institutions, regime", "conflict", "leaf")
    add("124", "Refuse to yield, not specified below", "conflict", "base")
    add("1241", "Refuse to ease administrative sanctions", "conflict", "leaf")
    add("1242", "Refuse to ease popular dissent", "conflict", "leaf")
    add("1243", "Refuse to release persons or property", "conflict", "leaf")
    add("1244", "Refuse to ease economic sanctions, boycott, or embargo", "conflict", "leaf")
    add("1245", "Refuse to allow international involvement (non mediation)", "conflict", "leaf")
    add("1246", "Refuse to de-escalate military engagement", "conflict", "leaf")
    add("125", "Reject proposal to meet, discuss, or negotiate", "conflict", "leaf")
    add("126", "Reject mediation", "conflict", "leaf")
    add("127", "Reject plan, agreement to settle dispute", "conflict", "leaf")
    add("128", "Defy norms, law", "conflict", "leaf")
    add("129", "Veto", "conflict", "leaf")
    
    add("13", "THREATEN", "conflict", "root")
    add("130", "Threaten, not specified below", "conflict", "base")
    add("131", "Threaten non-force, not specified below", "conflict", "base")
    add("1311", "Threaten to reduce or stop aid", "conflict", "leaf")
    add("1312", "Threaten to boycott, embargo, or sanction", "conflict", "leaf")
    add("1313", "Threaten to reduce or break relations", "conflict", "leaf")
    add("132", "Threaten with administrative sanctions, not specified below", "conflict", "base")
    add("1321", "Threaten to impose restrictions on political freedoms", "conflict", "leaf")
    add("1322", "Threaten to ban political parties or politicians", "conflict", "leaf")
    add("1323", "Threaten to impose curfew", "conflict", "leaf")
    add("1324", "Threaten to impose state of emergency or martial law", "conflict", "leaf")
    add("133", "Threaten political dissent, protest", "conflict", "leaf")
    add("134", "Threaten to halt negotiations", "conflict", "leaf")
    add("135", "Threaten to halt mediation", "conflict", "leaf")
    add("136", "Threaten to halt international involvement (non-mediation)", "conflict", "leaf")
    add("137", "Threaten with violent repression", "conflict", "leaf")
    add("138", "Threaten to use military force, not specified below", "conflict", "base")
    add("1381", "Threaten blockade", "conflict", "leaf")
    add("1382", "Threaten occupation", "conflict", "leaf")
    add("1383", "Threaten unconventional violence", "conflict", "leaf")
    add("1384", "Threaten conventional attack", "conflict", "leaf")
    add("1385", "Threaten attack with WMD", "conflict", "leaf")
    add("139", "Give ultimatum", "conflict", "leaf")
    
    add("14", "PROTEST", "conflict", "root")
    add("140", "Engage in political dissent, not specified below", "conflict", "base")
    add("141", "Demonstrate or rally", "conflict", "base")
    add("1411", "Demonstrate for leadership change", "conflict", "leaf")
    add("1412", "Demonstrate for policy change", "conflict", "leaf")
    add("1413", "Demonstrate for rights", "conflict", "leaf")
    add("1414", "Demonstrate for change in institutions, regime", "conflict", "leaf")
    add("142", "Conduct hunger strike, not specified below", "conflict", "base")
    add("1421", "Conduct hunger strike for leadership change", "conflict", "leaf")
    add("1422", "Conduct hunger strike for policy change", "conflict", "leaf")
    add("1423", "Conduct hunger strike for rights", "conflict", "leaf")
    add("1424", "Conduct hunger strike for change in institutions, regime", "conflict", "leaf")
    add("143", "Conduct strike or boycott, not specified below", "conflict", "base")
    add("1431", "Conduct strike or boycott for leadership change", "conflict", "leaf")
    add("1432", "Conduct strike or boycott for policy change", "conflict", "leaf")
    add("1433", "Conduct strike or boycott for rights", "conflict", "leaf")
    add("1434", "Conduct strike or boycott for change in institutions, regime", "conflict", "leaf")
    add("144", "Obstruct passage, block", "conflict", "base")
    add("1441", "Obstruct passage to demand leadership change", "conflict", "leaf")
    add("1442", "Obstruct passage to demand policy change", "conflict", "leaf")
    add("1443", "Obstruct passage to demand rights", "conflict", "leaf")
    add("1444", "Obstruct passage to demand change in institutions, regime", "conflict", "leaf")
    add("145", "Protest violently, riot", "conflict", "base")
    add("1451", "Engage in violent protest for leadership change", "conflict", "leaf")
    add("1452", "Engage in violent protest for policy change", "conflict", "leaf")
    add("1453", "Engage in violent protest for rights", "conflict", "leaf")
    add("1454", "Engage in violent protest for change in institutions, regime", "conflict", "leaf")
    
    add("15", "EXHIBIT FORCE POSTURE", "conflict", "root")
    add("150", "Demonstrate military or police power, not specified below", "conflict", "base")
    add("151", "Increase police alert status", "conflict", "leaf")
    add("152", "Increase military alert status", "conflict", "leaf")
    add("153", "Mobilize or increase police power", "conflict", "leaf")
    add("154", "Mobilize or increase armed forces", "conflict", "leaf")
    
    add("16", "REDUCE RELATIONS", "conflict", "root")
    add("160", "Reduce relations, not specified below", "conflict", "base")
    add("161", "Reduce or break diplomatic relations", "conflict", "leaf")
    add("162", "Reduce or stop aid, not specified below", "conflict", "base")
    add("1621", "Reduce or stop economic assistance", "conflict", "leaf")
    add("1622", "Reduce or stop military assistance", "conflict", "leaf")
    add("1623", "Reduce or stop humanitarian assistance", "conflict", "leaf")
    add("163", "Impose embargo, boycott, or sanctions", "conflict", "leaf")
    add("164", "Halt negotiations", "conflict", "leaf")
    add("165", "Halt mediation", "conflict", "leaf")
    add("166", "Expel or withdraw, not specified below", "conflict", "base")
    add("1661", "Expel or withdraw peacekeepers", "conflict", "leaf")
    add("1662", "Expel or withdraw inspectors, observers", "conflict", "leaf")
    add("1663", "Expel or withdraw aid agencies", "conflict", "leaf")
    
    add("17", "COERCE", "conflict", "root")
    add("170", "Coerce, not specified below", "conflict", "base")
    add("171", "Seize or damage property, not specified below", "conflict", "base")
    add("1711", "Confiscate property", "conflict", "leaf")
    add("1712", "Destroy property", "conflict", "leaf")
    add("172", "Impose administrative sanctions, not specified below", "conflict", "base")
    add("1721", "Impose restrictions on political freedoms", "conflict", "leaf")
    add("1722", "Ban political parties or politicians", "conflict", "leaf")
    add("1723", "Impose curfew", "conflict", "leaf")
    add("1724", "Impose state of emergency or martial law", "conflict", "leaf")
    add("173", "Arrest, detain, or charge with legal action", "conflict", "leaf")
    add("174", "Expel or deport individuals", "conflict", "leaf")
    add("175", "Use tactics of violent repression", "conflict", "leaf")
    
    add("18", "ASSAULT", "conflict", "root")
    add("180", "Use unconventional violence, not specified below", "conflict", "base")
    add("181", "Abduct, hijack, or take hostage", "conflict", "leaf")
    add("182", "Physically assault, not specified below", "conflict", "base")
    add("1821", "Sexually assault", "conflict", "leaf")
    add("1822", "Torture", "conflict", "leaf")
    add("1823", "Kill by physical assault", "conflict", "leaf")
    add("183", "Conduct suicide, car, or other non-military bombing, not specified below", "conflict", "base")
    add("1831", "Carry out suicide bombing", "conflict", "leaf")
    add("1832", "Carry out car bombing", "conflict", "leaf")
    add("1833", "Carry out roadside bombing", "conflict", "leaf")
    add("184", "Use as human shield", "conflict", "leaf")
    add("185", "Attempt to assassinate", "conflict", "leaf")
    add("186", "Assassinate", "conflict", "leaf")
    
    add("19", "FIGHT", "conflict", "root")
    add("190", "Use conventional military force, not specified below", "conflict", "base")
    add("191", "Impose blockade, restrict movement", "conflict", "leaf")
    add("192", "Occupy territory", "conflict", "leaf")
    add("193", "Fight with small arms and light weapons", "conflict", "leaf")
    add("194", "Fight with artillery and tanks", "conflict", "leaf")
    add("195", "Employ aerial weapons", "conflict", "leaf")
    add("196", "Violate ceasefire", "conflict", "leaf")
    
    add("20", "USE UNCONVENTIONAL MASS VIOLENCE", "conflict", "root")
    add("200", "Use unconventional mass violence, not specified below", "conflict", "base")
    add("201", "Engage in mass expulsion", "conflict", "leaf")
    add("202", "Engage in mass killings", "conflict", "leaf")
    add("203", "Engage in ethnic cleansing", "conflict", "leaf")
    add("204", "Use weapons of mass destruction, not specified below", "conflict", "base")
    add("2041", "Use chemical, biological, or radiological weapons", "conflict", "leaf")
    add("2042", "Detonate nuclear weapons", "conflict", "leaf")
    
    return codes


# Load codes once at module import
EVENT_CODES = _build_event_codes()


def get_event_code(code: str) -> Optional[EventCode]:
    """Get event code object by code."""
    return EVENT_CODES.get(code)


def search_event_codes(query: str) -> List[EventCode]:
    """Search event codes by description."""
    query_lower = query.lower()
    return [
        ec for ec in EVENT_CODES.values()
        if query_lower in ec.description.lower() or query_lower in ec.code
    ]


def get_codes_by_category(category: CategoryType) -> List[EventCode]:
    """Get all codes in a specific category."""
    return [ec for ec in EVENT_CODES.values() if ec.category == category]


def get_root_codes() -> List[EventCode]:
    """Get all root-level codes."""
    return [ec for ec in EVENT_CODES.values() if ec.level == "root"]


def get_quick_reference() -> str:
    """Get formatted quick reference for event codes."""
    return """
CAMEO Event Codes - Quick Reference

COOPERATION (Positive - Codes 01-08):
  01 - Make Public Statement
  02 - Appeal
  03 - Express Intent to Cooperate
  04 - Consult
  05 - Engage in Diplomatic Cooperation
  06 - Engage in Material Cooperation
  07 - Provide Aid
  08 - Yield

NEUTRAL/MIXED (Codes 09-13):
  09 - Investigate
  10 - Demand
  11 - Disapprove
  12 - Reject
  13 - Threaten

CONFLICT (Negative - Codes 14-20):
  14 - Protest
  15 - Exhibit Force Posture
  16 - Reduce Relations
  17 - Coerce
  18 - Assault
  19 - Fight (Conventional Military Force)
  20 - Use Unconventional Mass Violence

Total: 300+ specific event codes across 3 levels (root, base, leaf)
Usage: event_code, event_base_code, event_root_code
    """.strip()
