from typing import List, Optional
from .models import Heir, CaseState

# 1 Children, 2 Parents, 3 Grandchildren, 4 Siblings, 
# 5 Nephews, 6 Uncles, 7 Cousins, 8 Dhawu al-Arham, 9 Bayt al-Mal
PRIORITY_GROUPS = {
    "Children": ["Son", "Daughter"],
    "Parents": ["Father", "Mother"],
    "Grandchildren": ["Grandson", "Granddaughter"],
    "Siblings": ["Brother", "Sister"],
    "Nephews": ["Nephew", "Niece"],
    "Uncles": ["Uncle", "Aunt"],
    "Cousins": ["Cousin"],
    "Dhawu al-Arham": ["OtherRelative"],
    "Bayt al-Mal": ["State"]
}

PRIORITY_ORDER = [
    "Children", "Parents", "Grandchildren", "Siblings", 
    "Nephews", "Uncles", "Cousins", "Dhawu al-Arham", "Bayt al-Mal"
]

class PriorityResolver:
    @staticmethod
    def get_priority(relation: str) -> int:
        for i, group in enumerate(PRIORITY_ORDER):
            if relation in PRIORITY_GROUPS[group]:
                return i + 1
        return 99 # unknown

    @staticmethod
    def resolve_blocking(state: CaseState) -> CaseState:
        """
        Applies 'الأقرب يمنع الأبعد' (Nearest blocks distant).
        Some heirs (Husband/Wife/Parents) are never fully blocked from fixed shares,
        but they might be blocked from the remainder.
        For simplicity, this handles the core priority tree.
        """
        # Identify the highest priority present among non-fixed core groups
        highest_priority_group = None
        for group in PRIORITY_ORDER:
            if any(h.relation in PRIORITY_GROUPS[group] for h in state.heirs):
                highest_priority_group = group
                break
        
        if not highest_priority_group:
            return state

        # Fixed heirs (Husband, Wife, Father, Mother) generally always get their share
        # unless specifically blocked (like siblings by father).
        # We only block heirs who are strictly 'further' in the priority tree.
        
        # Determine the cutoff priority
        cutoff_priority = PRIORITY_ORDER.index(highest_priority_group)
        
        for heir in state.heirs:
            heir_priority = PriorityResolver.get_priority(heir.relation)
            if heir_priority > cutoff_priority + 1: # Group index is 0-based, priority is 1-based
                 # Special handling: Parents (priority 2) are never blocked by children (priority 1)
                 # because they have fixed shares (السدس).
                 if heir.relation in ["Father", "Mother"] and highest_priority_group == "Children":
                     continue
                 
                 # Husband and Wife are never blocked by anyone for their fixed shares.
                 if heir.relation in ["Husband", "Wife"]:
                     continue
                 
                 if heir.relation not in state.excluded_heirs:
                    state.excluded_heirs.append(heir.relation)
        
        return state
