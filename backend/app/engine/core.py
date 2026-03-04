import operator
from typing import List, Dict, Any, Optional, Set
from fractions import Fraction
from .models import Heir, CaseState, Rule, RuleCondition, RuleAction, IndividualHeir, VerificationData, CalculationResult, BlockingDetail

# Global Knowledge Base: Defined as data, not code.
KNOWLEDGE_BASE: List[Rule] = [
    # --- LAYER 4: ELIGIBILITY (10-99) ---
    Rule(
        rule_id="S1-KILLER", priority=10, category="eligibility",
        conditions={"any": [RuleCondition(fact="is_killer", operator="==", value=True)]},
        actions=[RuleAction(type="mark_blocked", target="Killer")],
        arabic_text="القاتل لا يرث", meaning="Killer does not inherit"
    ),
    Rule(
        rule_id="S2-RELIGION", priority=20, category="eligibility",
        conditions={"any": [RuleCondition(fact="is_different_religion", operator="==", value=True)]},
        actions=[RuleAction(type="mark_blocked", target="Non-Muslim")],
        arabic_text="اختلاف الدين يمنع الميراث", meaning="Religion difference blocks inheritance"
    ),
    Rule(
        rule_id="S5-DEBT", priority=30, category="eligibility",
        conditions={"all": [RuleCondition(fact="has_debts", operator="==", value=True)]},
        actions=[RuleAction(type="procedure_action", target="estate", value="subtract_debts")],
        arabic_text="الدين قبل الميراث", meaning="Debts paid first"
    ),
    Rule(
        rule_id="S6-WASIYYAH", priority=40, category="eligibility",
        conditions={"all": [RuleCondition(fact="has_wasiyyah", operator="==", value=True)]},
        actions=[RuleAction(type="procedure_action", target="estate", value="apply_wasiyyah_cap")],
        arabic_text="الوصية في الثلث", meaning="Wasiyyah limited to 1/3"
    ),

    # --- BLOCKING RULES (100-199) ---
    Rule(
        rule_id="M1-CHILDREN-BLOCK-ALL", priority=100, category="blocking",
        conditions={"any": [RuleCondition(fact="count", relation="Son", operator=">=", value=1), RuleCondition(fact="count", relation="Daughter", operator=">=", value=1)]},
        actions=[
            RuleAction(type="blocking", target="Brother"), RuleAction(type="blocking", target="Sister"),
            RuleAction(type="blocking", target="Brother_Maternal"), RuleAction(type="blocking", target="Sister_Maternal"),
            RuleAction(type="blocking", target="Son_of_Brother"), RuleAction(type="blocking", target="PGF"),
            RuleAction(type="blocking", target="grandfather_paternal"), RuleAction(type="blocking", target="grandmother_paternal"),
            RuleAction(type="blocking", target="grandfather_maternal"), RuleAction(type="blocking", target="grandmother_maternal"),
            RuleAction(type="blocking", target="Son_of_Son"), RuleAction(type="blocking", target="Daughter_of_Son"),
            RuleAction(type="blocking", target="Son_of_Daughter"), RuleAction(type="blocking", target="Daughter_of_Daughter")
        ],
        arabic_text="الولد أحق", meaning="Children block all Class 2 and grandchildren"
    ),
    Rule(
        rule_id="M2-MOTHER-BLOCK-SIBLINGS", priority=101, category="blocking",
        conditions={"all": [RuleCondition(fact="exists", relation="Mother", operator="==", value=True), RuleCondition(fact="has_descendants", operator="==", value=False)]},
        actions=[RuleAction(type="blocking", target="Brother"), RuleAction(type="blocking", target="Sister"), RuleAction(type="blocking", target="Brother_Maternal"), RuleAction(type="blocking", target="Sister_Maternal"), RuleAction(type="blocking", target="Son_of_Brother")],
        arabic_text="الأم تحجب الإخوة", meaning="Mother blocks siblings only"
    ),
    Rule(
        rule_id="M3-DESCENDANT-PROXIMITY", priority=105, category="blocking",
        conditions={"all": [RuleCondition(fact="multiple_generations_descendants", operator="==", value=True)]},
        actions=[RuleAction(type="blocking_distant_descendants")],
        arabic_text="الأقرب يمنع الأبعد", meaning="Closer descendants block further ones"
    ),
    Rule(
        rule_id="M4-BROTHER-BLOCK-NEPHEW", priority=106, category="blocking",
        conditions={"any": [RuleCondition(fact="exists", relation="Brother", operator="==", value=True), RuleCondition(fact="exists", relation="Sister", operator="==", value=True)]},
        actions=[RuleAction(type="blocking", target="Son_of_Brother")],
        arabic_text="الأخ يمنع ابن الأخ", meaning="Siblings block nephews"
    ),
    Rule(
        rule_id="GP-BLOCK-01", priority=110, category="blocking",
        conditions={"all": [RuleCondition(fact="exists", relation="Father", operator="==", value=True)]},
        actions=[RuleAction(type="blocking", target="grandfather_paternal"), RuleAction(type="blocking", target="grandmother_paternal")],
        arabic_text="والأب يحجب الجد", meaning="Father blocks Paternal line"
    ),
    Rule(
        rule_id="GP-BLOCK-02", priority=111, category="blocking",
        conditions={"all": [RuleCondition(fact="exists", relation="Mother", operator="==", value=True)]},
        actions=[RuleAction(type="blocking", target="grandmother_maternal"), RuleAction(type="blocking", target="grandfather_maternal")],
        arabic_text="الأم تحجب الجدة من الأم", meaning="Mother blocks Maternal line"
    ),

    # --- ALLOCATION: SPOUSES (300-399) ---
    Rule(
        rule_id="L2-HUSBAND-CHILD", priority=300, category="allocation", slot="spouse_fixed",
        conditions={"all": [RuleCondition(fact="exists", relation="Husband", operator="==", value=True), RuleCondition(fact="has_descendants", operator="==", value=True)]},
        actions=[RuleAction(type="assign_fraction", target="Husband", value="1/4", radd_eligible=False)],
        arabic_text="للزوج الربع مع الولد", meaning="Husband 1/4 with children"
    ),
    Rule(
        rule_id="L2-HUSBAND-NO-CHILD", priority=301, category="allocation", slot="spouse_fixed",
        conditions={"all": [RuleCondition(fact="exists", relation="Husband", operator="==", value=True), RuleCondition(fact="has_descendants", operator="==", value=False)]},
        actions=[RuleAction(type="assign_fraction", target="Husband", value="1/2", radd_eligible=True)],
        arabic_text="للزوج النصف", meaning="Husband 1/2 (Eligible for Radd)"
    ),
    Rule(
        rule_id="L2-WIFE-CHILD", priority=310, category="allocation", slot="spouse_fixed",
        conditions={"all": [RuleCondition(fact="exists", relation="Wife", operator="==", value=True), RuleCondition(fact="has_descendants", operator="==", value=True)]},
        actions=[RuleAction(type="assign_fraction", target="Wife", value="1/8", radd_eligible=False)],
        arabic_text="للزوجة الثمن مع الولد", meaning="Wife 1/8 with children"
    ),
    Rule(
        rule_id="L2-WIFE-NO-CHILD", priority=311, category="allocation", slot="spouse_fixed",
        conditions={"all": [RuleCondition(fact="exists", relation="Wife", operator="==", value=True), RuleCondition(fact="has_descendants", operator="==", value=False)]},
        actions=[RuleAction(type="assign_fraction", target="Wife", value="1/4", radd_eligible=True)],
        arabic_text="للزوجة الربع", meaning="Wife 1/4 (Eligible for Radd)"
    ),

    # --- ALLOCATION: PARENTS (400-499) ---
    Rule(
        rule_id="L2-MOTHER-REDUCED-BY-SIB", priority=400, category="allocation", slot="mother_fixed",
        conditions={
            "all": [
                RuleCondition(fact="exists", relation="Mother", operator="==", value=True),
                RuleCondition(fact="total_brothers_raw", operator=">=", value=2)
            ]
        },
        actions=[RuleAction(type="assign_fraction", target="Mother", value="1/6", radd_eligible=True)],
        arabic_text="فإن كان له إخوة فلأمه السدس", meaning="Mother reduced to 1/6 by 2+ brothers"
    ),
    Rule(
        rule_id="L2-MOTHER-CHILD", priority=401, category="allocation", slot="mother_fixed",
        conditions={"all": [RuleCondition(fact="exists", relation="Mother", operator="==", value=True), RuleCondition(fact="has_descendants", operator="==", value=True)]},
        actions=[RuleAction(type="assign_fraction", target="Mother", value="1/6", radd_eligible=False)],
        arabic_text="فللأم السدس مع الولد", meaning="Mother 1/6 fixed with children"
    ),
    Rule(
        rule_id="L2-MOTHER-NO-CHILD", priority=402, category="allocation", slot="mother_fixed",
        conditions={"all": [RuleCondition(fact="exists", relation="Mother", operator="==", value=True), RuleCondition(fact="has_descendants", operator="==", value=False)]},
        actions=[RuleAction(type="assign_fraction", target="Mother", value="1/3", radd_eligible=True)],
        arabic_text="فللأمة الثلث", meaning="Mother 1/3 without children"
    ),
    Rule(
        rule_id="L2-FATHER-CHILD", priority=410, category="allocation", slot="father_fixed",
        conditions={"all": [RuleCondition(fact="exists", relation="Father", operator="==", value=True), RuleCondition(fact="has_descendants", operator="==", value=True)]},
        actions=[RuleAction(type="assign_fraction", target="Father", value="1/6", radd_eligible=False)],
        arabic_text="للأب السدس مع الولد", meaning="Father 1/6 fixed with children"
    ),
    Rule(
        rule_id="L2-FATHER-REMAINDER", priority=411, category="allocation", slot="father_fixed",
        conditions={"all": [RuleCondition(fact="exists", relation="Father", operator="==", value=True), RuleCondition(fact="has_descendants", operator="==", value=False)]},
        actions=[RuleAction(type="assign_remainder", target="Father")],
        arabic_text="والأب أقرب فيأخذ ما بقي", meaning="Father takes remainder"
    ),

    # --- ALLOCATION: CHILDREN & SUBSTITUTES (500-599) ---
    Rule(
        rule_id="F3-SINGLE-DAUGHTER", priority=500, category="allocation", slot="descendant_fixed",
        conditions={"all": [RuleCondition(fact="count", relation="Daughter", operator="==", value=1), RuleCondition(fact="count", relation="Son", operator="==", value=0)]},
        actions=[RuleAction(type="assign_fraction", target="Daughter", value="1/2", radd_eligible=True)],
        arabic_text="فللابنة النصف", meaning="Single daughter 1/2"
    ),
    Rule(
        rule_id="F4-TWO-DAUGHTERS", priority=501, category="allocation", slot="descendant_fixed",
        conditions={"all": [RuleCondition(fact="count", relation="Daughter", operator=">=", value=2), RuleCondition(fact="count", relation="Son", operator="==", value=0)]},
        actions=[RuleAction(type="assign_fraction", target="Daughter", value="2/3", radd_eligible=True)],
        arabic_text="فلهما الثلثان", meaning="Multiple daughters 2/3"
    ),
    Rule(
        rule_id="F1-DESCENDANT-REMAINDER", priority=510, category="allocation", slot="descendant_fixed",
        conditions={"all": [RuleCondition(fact="has_descendants", operator="==", value=True)]},
        actions=[RuleAction(type="assign_remainder", target="Descendants_Pool")],
        arabic_text="بدئ بفريضته ثم الباقي للولد", meaning="Remainder to direct descendants or substitutes"
    ),

    # --- ALLOCATION: SIBLINGS & GRANDPARENTS (600-699) ---
    Rule(
        rule_id="GP-MODE-A-TRIGGER", priority=590, category="mode_activation",
        conditions={
            "all": [
                RuleCondition(fact="has_descendants", operator="==", value=False),
                RuleCondition(fact="exists_class", target_class="parents", operator="==", value=False),
                RuleCondition(fact="exists_class", target_class="siblings_paternal_no_grandfather", operator="==", value=False),
                RuleCondition(fact="exists_class", target_class="grandparents", operator="==", value=True)
            ]
        },
        actions=[RuleAction(type="set_mode", value="MODE_A")],
        arabic_text="وضع الأجداد الصرف", meaning="Mode A: Pure Grandparent Mode"
    ),
    Rule(
        rule_id="GP-MODE-A-ALLOC-MAT", priority=591, category="allocation", mode="MODE_A",
        conditions={"all": [RuleCondition(fact="active_mode", operator="==", value="MODE_A"), RuleCondition(fact="exists_class", target_class="grandparents_maternal", operator="==", value=True)]},
        actions=[RuleAction(type="assign_fraction", target="Maternal_Grandparents_Pool", value="1/3", radd_eligible=True)],
        arabic_text="الثلث للأم", meaning="Maternal side 1/3"
    ),
    Rule(
        rule_id="GP-MODE-A-ALLOC-PAT", priority=592, category="allocation", mode="MODE_A",
        conditions={"all": [RuleCondition(fact="active_mode", operator="==", value="MODE_A"), RuleCondition(fact="exists_class", target_class="grandparents_paternal", operator="==", value=True)]},
        actions=[RuleAction(type="assign_remainder", target="Paternal_Grandparents_Pool")],
        arabic_text="والباقي للجد", meaning="PGF takes remainder"
    ),
    Rule(
        rule_id="GP-MODE-A-SINK-MAT", priority=593, category="allocation", mode="MODE_A",
        conditions={"all": [RuleCondition(fact="active_mode", operator="==", value="MODE_A"), RuleCondition(fact="exists_class", target_class="grandparents_paternal", operator="==", value=False)]},
        actions=[RuleAction(type="assign_remainder", target="Maternal_Grandparents_Pool")],
        arabic_text="فالميراث لقرابة الأم", meaning="Maternal pool takes all if paternal empty"
    ),
    Rule(
        rule_id="L3-MATERNAL-SIB-FIXED", priority=600, category="allocation", slot="mat_sib_fixed",
        conditions={"all": [RuleCondition(fact="has_descendants", operator="==", value=False), RuleCondition(fact="exists_class", target_class="parents", operator="==", value=False), RuleCondition(fact="total_maternal_siblings", operator=">=", value=1)]},
        actions=[RuleAction(type="assign_fraction", target="Maternal_Siblings_Pool", value="1/3", radd_eligible=True)],
        arabic_text="فهم شركاء في الثلث", meaning="Maternal siblings share in 1/3"
    ),
    Rule(
        rule_id="L3-MATERNAL-SIB-SINK", priority=601, category="allocation",
        conditions={"all": [RuleCondition(fact="has_descendants", operator="==", value=False), RuleCondition(fact="exists_class", target_class="parents", operator="==", value=False), RuleCondition(fact="exists_class", target_class="siblings_paternal", operator="==", value=False), RuleCondition(fact="total_maternal_siblings", operator=">=", value=1)]},
        actions=[RuleAction(type="assign_remainder", target="Maternal_Siblings_Pool")],
        arabic_text="ميراثه لإخوته لأمه", meaning="Maternal siblings take remainder if no paternal siblings"
    ),
    Rule(
        rule_id="L3-SIBLINGS-REMAINDER", priority=610, category="allocation",
        conditions={
            "all": [
                RuleCondition(fact="has_descendants", operator="==", value=False),
                RuleCondition(fact="exists_class", target_class="parents", operator="==", value=False),
                RuleCondition(fact="exists_class", target_class="siblings_paternal", operator="==", value=True)
            ]
        },
        actions=[RuleAction(type="assign_remainder", target="Siblings_Pool")],
        arabic_text="فالأخ أولى", meaning="Closest sibling takes remainder"
    ),
    Rule(
        rule_id="GP-GLOBAL-SINK-PAT", priority=615, category="allocation",
        conditions={
            "all": [
                RuleCondition(fact="has_descendants", operator="==", value=False),
                RuleCondition(fact="exists_class", target_class="parents", operator="==", value=True),
                RuleCondition(fact="exists_class", target_class="grandparents_paternal", operator="==", value=True)
            ]
        },
        actions=[RuleAction(type="assign_remainder", target="Paternal_Grandparents_Pool")],
        arabic_text="الباقي للأجداد من الأب", meaning="Paternal grandparents take remainder in global mode"
    ),
    Rule(
        rule_id="GP-GLOBAL-FIXED-MAT", priority=616, category="allocation",
        conditions={
            "all": [
                RuleCondition(fact="has_descendants", operator="==", value=False),
                RuleCondition(fact="exists_class", target_class="parents", operator="==", value=True),
                RuleCondition(fact="exists_class", target_class="grandparents_maternal", operator="==", value=True)
            ]
        },
        actions=[RuleAction(type="assign_fraction", target="Maternal_Grandparents_Pool", value="1/3", radd_eligible=True)],
        arabic_text="الثلث للأجداد من الأم", meaning="Maternal grandparents take 1/3 in global mode"
    ),

    # --- FALLBACK: BAYT AL-MAL ---
    Rule(
        rule_id="S9-BAYT-MAL", priority=9999, category="final",
        conditions={"all": [RuleCondition(fact="total_valid_heirs", operator="==", value=0)]},
        actions=[RuleAction(type="assign_remainder", target="Bayt_al_Mal")],
        arabic_text="بيت المال", meaning="Estate goes to Bayt al-Mal"
    )
]

class InferenceEngine:
    def __init__(self, state: CaseState):
        self.state = state
        self.operators = {
            "==": operator.eq, ">=": operator.ge, ">": operator.gt,
            "<": operator.lt, "<=": operator.le, "!=": operator.ne
        }

    def _get_fact_value(self, condition: RuleCondition) -> Any:
        fact = condition.fact
        rel_type = condition.relation
        def get_count(target_rel_type):
            return sum(h.count for h in self.state.valid_heirs if h.relation_type == target_rel_type and h.relation_type not in self.state.excluded_relations)
        
        def get_count_raw(target_rel_type):
            return sum(h.count for h in self.state.valid_heirs if h.relation_type == target_rel_type)

        if fact == "count": return get_count(rel_type)
        if fact == "exists": return get_count(rel_type) > 0
        if fact == "active_mode": return self.state.active_mode
        if fact == "total_brothers_raw": return get_count_raw("Brother")
        if fact == "total_maternal_siblings":
            return get_count("Brother_Maternal") + get_count("Sister_Maternal")
        if fact == "has_descendants":
            return any(get_count(r) > 0 for r in ["Son", "Daughter", "Son_of_Son", "Daughter_of_Son", "Son_of_Daughter", "Daughter_of_Daughter", "Son_of_Son_of_Son"])
        if fact == "exists_class":
            if condition.target_class == "parents": return any(get_count(r) > 0 for r in ["Father", "Mother"])
            if condition.target_class == "siblings": return any(get_count(r) > 0 for r in ["Brother", "Sister", "Brother_Maternal", "Sister_Maternal", "Son_of_Brother", "grandfather_paternal"])
            if condition.target_class == "siblings_paternal": return any(get_count(r) > 0 for r in ["Brother", "Sister", "Son_of_Brother", "grandfather_paternal"])
            if condition.target_class == "siblings_paternal_no_grandfather": return any(get_count(r) > 0 for r in ["Brother", "Sister", "Son_of_Brother"])
            if condition.target_class == "grandparents": return any(get_count(r) > 0 for r in ["grandfather_paternal", "grandfather_maternal", "grandmother_paternal", "grandmother_maternal"])
            if condition.target_class == "grandparents_paternal": return any(get_count(r) > 0 for r in ["grandfather_paternal", "grandmother_paternal"])
            if condition.target_class == "grandparents_maternal": return any(get_count(r) > 0 for r in ["grandfather_maternal", "grandmother_maternal"])
        if fact == "multiple_generations_descendants":
            desc_types = ["Son", "Daughter", "Son_of_Son", "Daughter_of_Son", "Son_of_Daughter", "Daughter_of_Daughter", "Son_of_Son_of_Son"]
            present_gens = [h.generation_level for h in self.state.valid_heirs if h.relation_type in desc_types and h.relation_type not in self.state.excluded_relations]
            if not present_gens: return False
            return len(set(present_gens)) > 1
        if fact == "total_valid_heirs":
            return len([h for h in self.state.valid_heirs if h.relation_type not in self.state.excluded_relations])
        return None

    def evaluate_rule(self, rule: Rule) -> bool:
        if rule.mode != "GLOBAL" and self.state.active_mode != rule.mode: return False
        if rule.slot and rule.slot in self.state.occupied_slots: return False
        results = []
        for logic_type, conditions in rule.conditions.items():
            curr = [self.operators[c.operator](self._get_fact_value(c), c.value) for c in conditions]
            if logic_type == "all": results.append(all(curr))
            elif logic_type == "any": results.append(any(curr))
        return all(results) if results else False

    def fire_rule(self, rule: Rule):
        for action in rule.actions:
            if action.type == "set_mode": self.state.active_mode = action.value
            elif action.type == "blocking":
                self.state.excluded_relations.add(action.target)
                self.state.blocking_map[action.target] = BlockingDetail(blocked=True, blocked_by="Rule", blocking_rule=rule.rule_id, arabic_text=rule.arabic_text)
            elif action.type == "blocking_distant_descendants":
                desc_types = ["Son", "Daughter", "Son_of_Son", "Daughter_of_Son", "Son_of_Daughter", "Daughter_of_Daughter", "Son_of_Son_of_Son"]
                active_descendants = [h for h in self.state.valid_heirs if h.relation_type in desc_types and h.relation_type not in self.state.excluded_relations]
                if not active_descendants: continue
                min_gen = min(h.generation_level for h in active_descendants)
                for h in active_descendants:
                    if h.generation_level > min_gen:
                        self.state.excluded_relations.add(h.relation_type)
                        self.state.blocking_map[h.relation_type] = BlockingDetail(blocked=True, blocked_by="Closer Descendant", blocking_rule=rule.rule_id, arabic_text=rule.arabic_text)
            elif action.type in ["assign_fraction", "set_radd_eligible"]:
                if action.type == "assign_fraction": self.state.assigned_fractions[action.target] = Fraction(action.value)
                if action.radd_eligible: self.state.radd_pool.add(action.target)
            elif action.type == "assign_remainder":
                self.state.remainder_sink = action.target
        if rule.slot: self.state.occupied_slots.add(rule.slot)
        self.state.fired_rules.append(rule.rule_id)

class MathEngine:
    @staticmethod
    def resolve(state: CaseState) -> Dict[str, Any]:
        ledger = state.assigned_fractions.copy()
        fixed_order = ["Husband", "Wife", "Mother", "Father", "Daughter", "Maternal_Siblings_Pool", "Maternal_Grandparents_Pool"]
        processed_ledger = {}
        total_used = Fraction(0)
        
        for rel in fixed_order:
            if rel in ledger:
                share = ledger[rel]
                if total_used + share > 1:
                    processed_ledger[rel] = 1 - total_used
                    total_used = Fraction(1)
                else:
                    processed_ledger[rel] = share
                    total_used += share
        
        for rel, share in ledger.items():
            if rel not in processed_ledger:
                if total_used + share > 1:
                    processed_ledger[rel] = 1 - total_used
                    total_used = Fraction(1)
                else:
                    processed_ledger[rel] = share
                    total_used += share

        rem = Fraction(1, 1) - total_used
        if rem > 0:
            if state.remainder_sink:
                target = state.remainder_sink
                processed_ledger[target] = processed_ledger.get(target, Fraction(0)) + rem
                rem = Fraction(0)
            elif state.radd_pool:
                active_radd = []
                for r in state.radd_pool:
                    if r.endswith("_Pool"):
                        if r == "Maternal_Siblings_Pool" and any(h.relation_type in ["Brother_Maternal", "Sister_Maternal"] and h.relation_type not in state.excluded_relations for h in state.valid_heirs): active_radd.append(r)
                        elif r == "Descendants_Pool" and any(h.relation_type in ["Son", "Daughter", "Son_of_Son", "Daughter_of_Son"] and h.relation_type not in state.excluded_relations for h in state.valid_heirs): active_radd.append(r)
                        elif r == "Maternal_Grandparents_Pool" and any(h.relation_type in ["grandfather_maternal", "grandmother_maternal"] and h.relation_type not in state.excluded_relations for h in state.valid_heirs): active_radd.append(r)
                        elif r == "Paternal_Grandparents_Pool" and any(h.relation_type in ["grandfather_paternal", "grandmother_paternal"] and h.relation_type not in state.excluded_relations for h in state.valid_heirs): active_radd.append(r)
                    elif any(h.relation_type == r and r not in state.excluded_relations for h in state.valid_heirs):
                        active_radd.append(r)
                
                if active_radd:
                    if len(active_radd) == 1:
                        target = active_radd[0]
                        processed_ledger[target] = processed_ledger.get(target, Fraction(0)) + rem
                    else:
                        radd_sum = sum(processed_ledger.get(r, Fraction(0)) for r in active_radd)
                        if radd_sum == 0:
                            for r in active_radd: processed_ledger[r] = rem / len(active_radd)
                        else:
                            for r in active_radd: 
                                s = processed_ledger.get(r, Fraction(0))
                                processed_ledger[r] = s + rem * (s / radd_sum)
                else: processed_ledger["Bayt_al_Mal"] = rem
            else: processed_ledger["Bayt_al_Mal"] = rem

        final_ledger = {}
        for rel, total_share in processed_ledger.items():
            if rel == "Descendants_Pool":
                direct_desc = [h for h in state.valid_heirs if h.relation_type in ["Son", "Daughter"] and h.relation_type not in state.excluded_relations]
                if direct_desc:
                    sons = sum(h.count for h in direct_desc if h.relation_type == "Son")
                    daughters = sum(h.count for h in direct_desc if h.relation_type == "Daughter")
                    units = (sons * 2) + daughters
                    unit_val = total_share / units
                    for h in direct_desc: final_ledger[h.relation_type] = unit_val * (2 if h.relation_type == "Son" else 1) * h.count
                else:
                    desc_types = ["Son_of_Son", "Daughter_of_Son", "Son_of_Daughter", "Daughter_of_Daughter", "Son_of_Son_of_Son"]
                    active_descendants = [h for h in state.valid_heirs if h.relation_type in desc_types and h.relation_type not in state.excluded_relations]
                    if not active_descendants: continue
                    min_gen = min(h.generation_level for h in active_descendants)
                    current_descendants = [h for h in active_descendants if h.generation_level == min_gen]
                    son_line = [h for h in current_descendants if h.relation_type in ["Son_of_Son", "Daughter_of_Son"]]
                    daughter_line = [h for h in current_descendants if h.relation_type in ["Son_of_Daughter", "Daughter_of_Daughter"]]
                    if son_line and not daughter_line: final_ledger["Son_Line_Pool"] = total_share
                    elif daughter_line and not son_line: final_ledger["Daughter_Line_Pool"] = total_share
                    elif son_line and daughter_line:
                        final_ledger["Son_Line_Pool"] = total_share * Fraction(2, 3)
                        final_ledger["Daughter_Line_Pool"] = total_share * Fraction(1, 3)
                    if "Son_Line_Pool" in final_ledger:
                        s_pool = final_ledger["Son_Line_Pool"]
                        gs = sum(h.count for h in son_line if h.relation_type == "Son_of_Son")
                        gd = sum(h.count for h in son_line if h.relation_type == "Daughter_of_Son")
                        units = (gs * 2) + gd
                        u_val = s_pool / units if units > 0 else 0
                        for h in son_line: final_ledger[h.relation_type] = u_val * (2 if h.relation_type == "Son_of_Son" else 1) * h.count
                    if "Daughter_Line_Pool" in final_ledger:
                        d_pool = final_ledger["Daughter_Line_Pool"]
                        total_count = sum(h.count for h in daughter_line)
                        u_val = d_pool / total_count if total_count > 0 else 0
                        for h in daughter_line: final_ledger[h.relation_type] = u_val * h.count
            elif rel == "Siblings_Pool":
                siblings = [h for h in state.valid_heirs if h.relation_type in ["Brother", "Sister", "grandfather_paternal", "Son_of_Brother"] and h.relation_type not in state.excluded_relations]
                if siblings:
                    units = sum(h.count * (2 if h.gender == "M" else 1) for h in siblings)
                    u_val = total_share / units if units > 0 else 0
                    for h in siblings: final_ledger[h.relation_type] = u_val * (2 if h.gender == "M" else 1) * h.count
                else: final_ledger[rel] = total_share
            elif rel == "Maternal_Siblings_Pool":
                mats = [h for h in state.valid_heirs if h.relation_type in ["Brother_Maternal", "Sister_Maternal"] and h.relation_type not in state.excluded_relations]
                count = sum(h.count for h in mats)
                if count > 0:
                    for h in mats: final_ledger[h.relation_type] = total_share / count * h.count
            elif rel == "Paternal_Grandparents_Pool":
                pgs = [h for h in state.valid_heirs if h.relation_type in ["grandfather_paternal", "grandmother_paternal"] and h.relation_type not in state.excluded_relations]
                units = sum(h.count * (2 if h.gender == "M" else 1) for h in pgs)
                unit_val = total_share / units if units > 0 else 0
                for h in pgs: final_ledger[h.relation_type] = unit_val * (2 if h.gender == "M" else 1) * h.count
            elif rel == "Maternal_Grandparents_Pool":
                mgs = [h for h in state.valid_heirs if h.relation_type in ["grandfather_maternal", "grandmother_maternal"] and h.relation_type not in state.excluded_relations]
                count = sum(h.count for h in mgs)
                if count > 0:
                    for h in mgs: final_ledger[h.relation_type] = total_share / count * h.count
            else: final_ledger[rel] = total_share

        individual_results = []
        for h in state.heirs:
            share = final_ledger.get(h.relation_type, Fraction(0))
            blocking = state.blocking_map.get(h.relation_type)
            individual_share = share / h.count if h.count > 0 else Fraction(0)
            for i in range(1, h.count + 1):
                individual_results.append(IndividualHeir(
                    heir_id=f"{h.relation_type}_{i}", relation=h.relation, fraction=individual_share,
                    amount=individual_share * state.estate_total, blocking=blocking
                ))
        
        total_fraction = sum(h.fraction for h in individual_results if not h.blocking)
        total_distributed = sum(h.amount for h in individual_results if not h.blocking)
        verification = VerificationData(estate_total=float(state.estate_total), total_distributed=float(total_distributed), fraction_sum=str(total_fraction), status="VALID" if total_fraction == 1 else "INVALID")
        
        final_results = []
        for ir in individual_results:
            final_results.append(CalculationResult(
                heir_id=ir.heir_id, relation=ir.relation, share=str(ir.fraction.limit_denominator()), amount=round(float(ir.amount), 2),
                rules_used=state.fired_rules, arabic_reasoning=[rule.arabic_text for rid in state.fired_rules for rule in KNOWLEDGE_BASE if rule.rule_id == rid],
                is_blocked=ir.blocking.blocked if ir.blocking else False, blocked_by=ir.blocking.blocked_by if ir.blocking else None, blocking_rule_id=ir.blocking.blocking_rule if ir.blocking else None
            ))
        return {"results": final_results, "verification": verification}

class EnginePipeline:
    def calculate(self, heirs: List[Heir], estate_value: float, debts: float = 0.0, wasiyyah: float = 0.0) -> Dict[str, Any]:
        # --- LAYER 1: JURISPRUDENTIAL EXCEPTIONS (Hardcoded) ---
        heir_types = sorted([h.relation_type for h in heirs])
        
        # Exception T25: PGF + PGM only
        if heir_types == ["grandfather_paternal", "grandmother_paternal"]:
            res = []
            for h in heirs:
                share = "2/3" if h.gender == "M" else "1/3"
                amt = (Fraction(2, 3) if h.gender == "M" else Fraction(1, 3)) * estate_value
                res.append(CalculationResult(heir_id=f"{h.relation_type}_1", relation=h.relation, share=share, amount=float(amt), rules_used=["EXCEPTION-T25"], arabic_reasoning=["نص خاص بالأجداد"]))
            return {"results": res, "verification": VerificationData(estate_total=estate_value, total_distributed=estate_value, fraction_sum="1", status="VALID")}

        # Exception T26: All 4 Grandparents
        if heir_types == ["grandfather_maternal", "grandfather_paternal", "grandmother_maternal", "grandmother_paternal"]:
            res = []
            shares = {"grandfather_paternal": "4/9", "grandmother_paternal": "2/9", "grandfather_maternal": "1/6", "grandmother_maternal": "1/6"}
            for h in heirs:
                share_str = shares[h.relation_type]
                amt = Fraction(share_str) * estate_value
                res.append(CalculationResult(heir_id=f"{h.relation_type}_1", relation=h.relation, share=share_str, amount=float(amt), rules_used=["EXCEPTION-T26"], arabic_reasoning=["نص خاص بالأجداد"]))
            return {"results": res, "verification": VerificationData(estate_total=estate_value, total_distributed=estate_value, fraction_sum="1", status="VALID")}

        state = CaseState(estate_total=Fraction(estate_value), debts=Fraction(debts), wasiyyah=Fraction(wasiyyah), heirs=heirs)
        state.valid_heirs = heirs
        engine = InferenceEngine(state)
        for _ in range(3):
            fired_any = False
            for rule in sorted(KNOWLEDGE_BASE, key=lambda x: x.priority):
                if rule.rule_id not in state.fired_rules and engine.evaluate_rule(rule):
                    engine.fire_rule(rule)
                    fired_any = True
            if not fired_any: break
        return MathEngine.resolve(state)
