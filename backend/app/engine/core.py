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
        rule_id="GP-BLOCK-01", priority=100, category="blocking",
        conditions={"all": [RuleCondition(fact="exists", relation="Father", operator="==", value=True)]},
        actions=[RuleAction(type="blocking", target="grandfather_paternal"), RuleAction(type="blocking", target="grandmother_paternal")],
        arabic_text="والأب يحجب الجد", meaning="Father blocks Paternal Grandparents."
    ),
    Rule(
        rule_id="GP-BLOCK-02", priority=101, category="blocking",
        conditions={"all": [RuleCondition(fact="exists", relation="Mother", operator="==", value=True)]},
        actions=[RuleAction(type="blocking", target="grandmother_maternal")],
        arabic_text="الأم تحجب الجدة من الأم", meaning="Mother blocks Maternal Grandmother."
    ),
    Rule(
        rule_id="GP-BLOCK-03-PGM", priority=102, category="blocking",
        conditions={"all": [RuleCondition(fact="multiple_generations", relation="grandmother_paternal", operator="==", value=True)]},
        actions=[RuleAction(type="blocking_distant", target="grandmother_paternal")],
        arabic_text="الأقرب يمنع الأبعد", meaning="Closest paternal grandmother blocks distant ones."
    ),
    Rule(
        rule_id="GP-BLOCK-03-MGM", priority=103, category="blocking",
        conditions={"all": [RuleCondition(fact="multiple_generations", relation="grandmother_maternal", operator="==", value=True)]},
        actions=[RuleAction(type="blocking_distant", target="grandmother_maternal")],
        arabic_text="الأقرب يمنع الأبعد", meaning="Closest maternal grandmother blocks distant ones."
    ),

    # --- MODE ACTIVATION (200-299) ---
    Rule(
        rule_id="GP-MODE-A-TRIGGER", priority=200, category="mode_activation",
        conditions={
            "all": [
                RuleCondition(fact="has_descendants", operator="==", value=False),
                RuleCondition(fact="exists_class", target_class="parents", operator="==", value=False),
                RuleCondition(fact="exists_class", target_class="siblings", operator="==", value=False),
                RuleCondition(fact="exists_class", target_class="grandparents", operator="==", value=True)
            ]
        },
        actions=[RuleAction(type="set_mode", value="MODE_A")],
        arabic_text="وضع الأجداد الصرف", meaning="Mode A: Pure Grandparent Mode"
    ),
    Rule(
        rule_id="GP-MODE-B-TRIGGER", priority=210, category="mode_activation",
        conditions={
            "all": [
                RuleCondition(fact="exists", relation="grandfather_paternal", operator="==", value=True),
                RuleCondition(fact="exists_class", target_class="siblings_maternal", operator="==", value=True),
                RuleCondition(fact="exists", relation="Father", operator="==", value=False),
                RuleCondition(fact="has_descendants", operator="==", value=False)
            ]
        },
        actions=[RuleAction(type="set_mode", value="MODE_B")],
        arabic_text="الجد مع الإخوة للأم", meaning="Mode B: PGF + Maternal Siblings Mode"
    ),
    Rule(
        rule_id="GP-MODE-C-TRIGGER", priority=220, category="mode_activation",
        conditions={
            "all": [
                RuleCondition(fact="exists", relation="grandfather_paternal", operator="==", value=True),
                RuleCondition(fact="exists", relation="Son_of_Brother", operator="==", value=True),
                RuleCondition(fact="exists", relation="Father", operator="==", value=False),
                RuleCondition(fact="has_descendants", operator="==", value=False)
            ]
        },
        actions=[RuleAction(type="set_mode", value="MODE_C")],
        arabic_text="الجد مع ابن الأخ", meaning="Mode C: PGF + Nephew Mode"
    ),

    # --- ALLOCATION RULES (300-899) ---
    Rule(
        rule_id="L2-MOTHER-NO-CHILD", priority=300, category="allocation", slot="mother_fixed",
        conditions={"all": [RuleCondition(fact="exists", relation="Mother", operator="==", value=True), RuleCondition(fact="has_descendants", operator="==", value=False)]},
        actions=[RuleAction(type="assign_fraction", target="Mother", value="1/3", radd_eligible=True)],
        arabic_text="فللأمة الثلث إذا لم يكن ولد", meaning="Mother 1/3 without descendants"
    ),
    Rule(
        rule_id="L2-FATHER-REMAINDER", priority=310, category="allocation", slot="father_fixed",
        conditions={"all": [RuleCondition(fact="exists", relation="Father", operator="==", value=True), RuleCondition(fact="has_descendants", operator="==", value=False)]},
        actions=[RuleAction(type="assign_remainder", target="Father")],
        arabic_text="والأب أقرب فيأخذ ما بقي", meaning="Father takes remainder without descendants"
    ),
    Rule(
        rule_id="F1-DAUGHTER-FIXED", priority=320, category="allocation", slot="descendant_fixed",
        conditions={"all": [RuleCondition(fact="exists", relation="Daughter", operator="==", value=True), RuleCondition(fact="count", relation="Son", operator="==", value=0)]},
        actions=[RuleAction(type="assign_fraction", target="Daughter", value="1/2", radd_eligible=True)],
        arabic_text="فللابنة النصف", meaning="Single daughter 1/2"
    ),
    Rule(
        rule_id="GP-MODE-A-ALLOC", priority=330, category="allocation", mode="MODE_A",
        conditions={"all": [RuleCondition(fact="active_mode", operator="==", value="MODE_A")]},
        actions=[
            RuleAction(type="assign_fraction", target="Maternal_Grandparents_Pool", value="1/3", radd_eligible=True),
            RuleAction(type="assign_remainder", target="Paternal_Grandparents_Pool")
        ],
        arabic_text="الثلث لقرابة الأم والثلثان لقرابة الأب", meaning="Maternal side 1/3, Paternal side 2/3"
    ),
    Rule(
        rule_id="GP-MODE-B-ALLOC", priority=400, category="allocation", mode="MODE_B",
        conditions={"all": [RuleCondition(fact="active_mode", operator="==", value="MODE_B")]},
        actions=[
            RuleAction(type="assign_fraction", target="Maternal_Siblings_Pool", value="1/3", radd_eligible=True),
            RuleAction(type="assign_remainder", target="grandfather_paternal")
        ],
        arabic_text="كان للإخوة الثلث والباقي للجد", meaning="Maternal siblings 1/3, PGF takes remainder"
    ),
    Rule(
        rule_id="GP-MODE-C-ALLOC", priority=500, category="allocation", mode="MODE_C",
        conditions={"all": [RuleCondition(fact="active_mode", operator="==", value="MODE_C")]},
        actions=[
            RuleAction(type="substitute_relation", source="Son_of_Brother", as_relation="Brother"),
            RuleAction(type="assign_remainder", target="PGF_Brother_Pool")
        ],
        arabic_text="وابن الأخ يرث مع الجد ميراث أبيه", meaning="Nephew substitutes brother, shares with PGF"
    ),
    Rule(
        rule_id="GP-MODE-D-PGM", priority=600, category="allocation",
        conditions={
            "all": [
                RuleCondition(fact="exists", relation="grandmother_paternal", operator="==", value=True),
                RuleCondition(fact="is_blocked", relation="grandmother_paternal", operator="==", value=False),
                RuleCondition(fact="has_primary_heirs", operator="==", value=True)
            ]
        },
        actions=[RuleAction(type="assign_fraction", target="grandmother_paternal", value="1/6", radd_eligible=False)],
        arabic_text="للجدة من الأب السدس", meaning="PGM gets fixed 1/6 when primary heirs present"
    ),
    Rule(
        rule_id="GP-MODE-D-MGM", priority=610, category="allocation",
        conditions={
            "all": [
                RuleCondition(fact="exists", relation="grandmother_maternal", operator="==", value=True),
                RuleCondition(fact="is_blocked", relation="grandmother_maternal", operator="==", value=False),
                RuleCondition(fact="has_primary_heirs", operator="==", value=True)
            ]
        },
        actions=[RuleAction(type="assign_fraction", target="grandmother_maternal", value="1/6", radd_eligible=False)],
        arabic_text="للجدة من الأم السدس", meaning="MGM gets fixed 1/6 when primary heirs present"
    ),

    # --- RADD OVERRIDES (900-999) ---
    Rule(
        rule_id="GP-RADD-OVERRIDE", priority=900, category="allocation",
        conditions={
            "all": [
                RuleCondition(fact="has_primary_heirs", operator="==", value=True),
                RuleCondition(fact="exists_class", target_class="grandparents", operator="==", value=True)
            ]
        },
        actions=[RuleAction(type="set_radd_eligible", target="grandparents", radd_eligible=False)],
        arabic_text="ولا يرد على الجدتين شيء", meaning="No radd to grandmothers with primary heirs"
    ),
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
            if target_rel_type in self.state.excluded_relations: return 0
            return sum(h.count for h in self.state.valid_heirs if h.relation_type == target_rel_type and h.relation_type not in self.state.excluded_relations)

        if fact == "count": return get_count(rel_type)
        if fact == "exists": return get_count(rel_type) > 0
        if fact == "active_mode": return self.state.active_mode
        if fact == "is_blocked": return rel_type in self.state.excluded_relations
        if fact == "has_wasiyyah": return self.state.wasiyyah > 0
        if fact == "has_debts": return self.state.debts > 0
        if fact == "has_descendants":
            return any(get_count(r) > 0 for r in ["Son", "Daughter", "Son_of_Son", "Daughter_of_Son", "Son_of_Daughter", "Daughter_of_Daughter"])
        if fact == "exists_class":
            if condition.target_class == "parents": return any(get_count(r) > 0 for r in ["Father", "Mother"])
            if condition.target_class == "siblings": return any(get_count(r) > 0 for r in ["Brother", "Sister"])
            if condition.target_class == "siblings_maternal": return any(get_count(r) > 0 for r in ["Brother_Maternal", "Sister_Maternal", "Son_of_Brother_Maternal"])
            if condition.target_class == "grandparents": return any(get_count(r) > 0 for r in ["grandfather_paternal", "grandfather_maternal", "grandmother_paternal", "grandmother_maternal"])
        if fact == "has_primary_heirs":
            return any(get_count(r) > 0 for r in ["Son", "Daughter", "Father", "Mother", "Husband", "Wife"])
        if fact == "multiple_generations":
            heirs = [h for h in self.state.valid_heirs if h.relation_type == rel_type]
            if not heirs: return False
            min_gen = min(h.generation_level for h in heirs)
            return any(h.generation_level > min_gen for h in heirs)
        if fact == "total_valid_heirs":
            return len([h for h in self.state.valid_heirs if h.relation_type not in self.state.excluded_relations])
        return None

    def evaluate_rule(self, rule: Rule) -> bool:
        if rule.mode != "GLOBAL" and self.state.active_mode != rule.mode: return False
        if rule.slot and rule.slot in self.state.occupied_slots: return False
        results = []
        for logic_type, conditions in rule.conditions.items():
            current_results = []
            for cond in conditions:
                fact_val = self._get_fact_value(cond)
                current_results.append(self.operators[cond.operator](fact_val, cond.value))
            if logic_type == "all": results.append(all(current_results))
            elif logic_type == "any": results.append(any(current_results))
        return all(results) if results else False

    def fire_rule(self, rule: Rule):
        for action in rule.actions:
            if action.type == "set_mode":
                self.state.active_mode = action.value
            elif action.type == "blocking":
                self.state.excluded_relations.add(action.target)
                self.state.blocking_map[action.target] = BlockingDetail(blocked=True, blocked_by="Rule", blocking_rule=rule.rule_id, arabic_text=rule.arabic_text)
            elif action.type == "blocking_distant":
                min_gen = min(h.generation_level for h in self.state.valid_heirs if h.relation_type == action.target)
                for h in self.state.valid_heirs:
                    if h.relation_type == action.target and h.generation_level > min_gen:
                        heir_id = f"{h.relation_type}_{h.generation_level}"
                        self.state.excluded_relations.add(heir_id)
                        self.state.blocking_map[heir_id] = BlockingDetail(blocked=True, blocked_by="Closer kin", blocking_rule=rule.rule_id, arabic_text=rule.arabic_text)
            elif action.type in ["assign_fraction", "set_radd_eligible"]:
                if action.type == "assign_fraction": self.state.assigned_fractions[action.target] = Fraction(action.value)
                targets = ["grandfather_paternal", "grandfather_maternal", "grandmother_paternal", "grandmother_maternal"] if action.target == "grandparents" else [action.target]
                for t in targets:
                    if action.radd_eligible: self.state.radd_pool.add(t)
                    elif t in self.state.radd_pool: self.state.radd_pool.discard(t)
            elif action.type == "assign_remainder":
                self.state.remainder_sink = action.target
            elif action.type == "substitute_relation":
                self.state.virtual_mappings[action.source] = action.as_relation
        if rule.slot: self.state.occupied_slots.add(rule.slot)
        self.state.fired_rules.append(rule.rule_id)

class MathEngine:
    @staticmethod
    def resolve(state: CaseState) -> Dict[str, Any]:
        ledger = state.assigned_fractions.copy()
        potential_pools = ["PGF_Brother_Pool", "Paternal_Grandparents_Pool", "Maternal_Grandparents_Pool", "Maternal_Siblings_Pool"]
        for p in potential_pools:
            if p not in ledger: ledger[p] = Fraction(0)
        
        fixed_sum = sum(ledger.values())
        rem = Fraction(1, 1) - fixed_sum
        
        if rem > 0:
            if state.remainder_sink:
                ledger[state.remainder_sink] = ledger.get(state.remainder_sink, Fraction(0)) + rem
                rem = Fraction(0)
            else:
                active_radd = [r for r in state.radd_pool if (r in ledger or r.endswith("_Pool"))]
                if active_radd:
                    radd_sum = sum(ledger.get(r, Fraction(0)) for r in active_radd)
                    if radd_sum == 0:
                        for r in active_radd: ledger[r] += rem / len(active_radd)
                    else:
                        for r in active_radd: ledger[r] += rem * (ledger[r] / radd_sum)
                    rem = Fraction(0)

        if rem > 0:
             present_pools = [p for p in potential_pools if (p == "PGF_Brother_Pool" and any(h.relation_type in ["grandfather_paternal", "Son_of_Brother"] for h in state.valid_heirs)) or 
                              (p == "Paternal_Grandparents_Pool" and any(h.relation_type in ["grandfather_paternal", "grandmother_paternal"] for h in state.valid_heirs)) or
                              (p == "Maternal_Grandparents_Pool" and any(h.relation_type in ["grandfather_maternal", "grandmother_maternal"] for h in state.valid_heirs)) or
                              (p == "Maternal_Siblings_Pool" and any(h.relation_type in ["Brother_Maternal", "Sister_Maternal"] for h in state.valid_heirs))]
             if present_pools:
                 sink = present_pools[0]
                 if "Paternal_Grandparents_Pool" in present_pools: sink = "Paternal_Grandparents_Pool"
                 ledger[sink] += rem
             else:
                 unblocked = [h.relation_type for h in state.valid_heirs if h.relation_type not in state.excluded_relations]
                 if unblocked: ledger[unblocked[0]] = ledger.get(unblocked[0], Fraction(0)) + rem

        final_individual_shares = {}
        for rel, total_share in ledger.items():
            if rel.endswith("_Pool"):
                sub_heirs = []
                if rel == "Maternal_Grandparents_Pool": sub_heirs = [h for h in state.valid_heirs if h.relation_type in ["grandfather_maternal", "grandmother_maternal"] and h.relation_type not in state.excluded_relations]
                elif rel == "Paternal_Grandparents_Pool": sub_heirs = [h for h in state.valid_heirs if h.relation_type in ["grandfather_paternal", "grandmother_paternal"] and h.relation_type not in state.excluded_relations]
                elif rel == "Maternal_Siblings_Pool": sub_heirs = [h for h in state.valid_heirs if h.relation_type in ["Brother_Maternal", "Sister_Maternal"] and h.relation_type not in state.excluded_relations]
                elif rel == "PGF_Brother_Pool": sub_heirs = [h for h in state.valid_heirs if h.relation_type in ["grandfather_paternal", "Son_of_Brother"] and h.relation_type not in state.excluded_relations]
                
                if sub_heirs:
                    if rel in ["Paternal_Grandparents_Pool", "PGF_Brother_Pool"]:
                        units = sum(h.count * (2 if h.gender == "M" else 1) for h in sub_heirs)
                        unit_val = total_share / units
                        for h in sub_heirs: final_individual_shares[h.relation_type] = final_individual_shares.get(h.relation_type, Fraction(0)) + unit_val * (2 if h.gender == "M" else 1)
                    else:
                        total_count = sum(h.count for h in sub_heirs)
                        for h in sub_heirs: final_individual_shares[h.relation_type] = final_individual_shares.get(h.relation_type, Fraction(0)) + total_share / total_count
            else:
                final_individual_shares[rel] = final_individual_shares.get(rel, Fraction(0)) + total_share

        individual_results = []
        for h in state.heirs:
            heir_blocked_key = f"{h.relation_type}_{h.generation_level}"
            blocking = state.blocking_map.get(heir_blocked_key) or state.blocking_map.get(h.relation_type)
            share = final_individual_shares.get(h.relation_type, Fraction(0)) if not blocking else Fraction(0)
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
