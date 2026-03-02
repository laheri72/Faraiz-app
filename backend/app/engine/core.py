import operator
from typing import List, Dict, Any, Optional
from fractions import Fraction
from .models import Heir, CaseState, Rule, RuleCondition, RuleAction, IndividualHeir, VerificationData, CalculationResult

# Global Knowledge Base: Defined as data, not code.
KNOWLEDGE_BASE: List[Rule] = [
    # --- LAYER 4: ELIGIBILITY ---
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

    # --- LAYER 1: SUBSTITUTION ---
    Rule(
        rule_id="V6-GRANDCHILD-SUBSTITUTE", priority=100, category="substitution",
        conditions={
            "all": [
                RuleCondition(fact="count", relation="Son", operator="==", value=0),
                RuleCondition(fact="count", relation="Daughter", operator="==", value=0),
                RuleCondition(fact="exists", relation="Grandson", operator="==", value=True)
            ]
        },
        actions=[RuleAction(type="substitute_relation", source="Grandson", as_relation="Son")],
        arabic_text="ولد الولد يقوم مقام الولد", meaning="Grandchildren substitute children if children absent"
    ),

    # --- LAYER 2: CLASS 1 (DESCENDANTS & PARENTS) ---
    Rule(
        rule_id="F2-SINGLE-SON", priority=500, category="allocation", slot="descendant_fixed",
        conditions={
            "all": [
                RuleCondition(fact="count", relation="Son", operator="==", value=1),
                RuleCondition(fact="count", relation="Daughter", operator="==", value=0)
            ]
        },
        actions=[RuleAction(type="assign_remainder", target="Son")],
        arabic_text="فإن لم يترك غير ولد واحد ذكر فالميراث له كله", meaning="Single son receives everything"
    ),
    Rule(
        rule_id="F3-SINGLE-DAUGHTER", priority=510, category="allocation", slot="descendant_fixed",
        conditions={
            "all": [
                RuleCondition(fact="count", relation="Daughter", operator="==", value=1),
                RuleCondition(fact="count", relation="Son", operator="==", value=0)
            ]
        },
        actions=[RuleAction(type="assign_fraction", target="Daughter", value="1/2", radd_eligible=True)],
        arabic_text="فللابنة النصف بالميراث المسمى ويرد عليها", meaning="Single daughter receives 1/2 fixed and proportional Radd"
    ),
    Rule(
        rule_id="F4-DAUGHTERS-ONLY", priority=520, category="allocation", slot="descendant_fixed",
        conditions={
            "all": [
                RuleCondition(fact="count", relation="Daughter", operator=">=", value=2),
                RuleCondition(fact="count", relation="Son", operator="==", value=0)
            ]
        },
        actions=[RuleAction(type="assign_fraction", target="Daughter", value="2/3", radd_eligible=True)],
        arabic_text="فلكل واحدة الثلث بالميراث ويرد عليهما", meaning="Multiple daughters share 2/3 fixed and proportional Radd"
    ),
    Rule(
        rule_id="F1-SON-DAUGHTER", priority=530, category="allocation", slot="descendant_fixed",
        conditions={
            "all": [
                RuleCondition(fact="count", relation="Son", operator=">=", value=1),
                RuleCondition(fact="count", relation="Daughter", operator=">=", value=1)
            ]
        },
        actions=[RuleAction(type="assign_remainder", target="Children")],
        arabic_text="للذكر مثل حظ الأنثيين", meaning="Sons and daughters share remainder in 2:1 ratio"
    ),

    # --- LAYER 2: SPOUSES ---
    Rule(
        rule_id="L2-HUSBAND-CHILD", priority=600, category="allocation", slot="spouse_fixed",
        conditions={"all": [RuleCondition(fact="exists", relation="Husband", operator="==", value=True), RuleCondition(fact="has_descendants", operator="==", value=True)]},
        actions=[RuleAction(type="assign_fraction", target="Husband", value="1/4", radd_eligible=False)],
        arabic_text="للزوج الربع مع الولد", meaning="Husband receives 1/4 when descendants exist"
    ),
    Rule(
        rule_id="L2-HUSBAND-NO-CHILD", priority=610, category="allocation", slot="spouse_fixed",
        conditions={"all": [RuleCondition(fact="exists", relation="Husband", operator="==", value=True), RuleCondition(fact="has_descendants", operator="==", value=False)]},
        actions=[RuleAction(type="assign_fraction", target="Husband", value="1/2", radd_eligible=False)],
        arabic_text="للزوج النصف إذا لم يكن ولد", meaning="Husband receives 1/2 when no descendants exist"
    ),
    Rule(
        rule_id="L2-WIFE-CHILD", priority=620, category="allocation", slot="spouse_fixed",
        conditions={"all": [RuleCondition(fact="exists", relation="Wife", operator="==", value=True), RuleCondition(fact="has_descendants", operator="==", value=True)]},
        actions=[RuleAction(type="assign_fraction", target="Wife", value="1/8", radd_eligible=False)],
        arabic_text="للزوجة الثمن مع الولد", meaning="Wife receives 1/8 when descendants exist"
    ),
    Rule(
        rule_id="L2-WIFE-NO-CHILD", priority=630, category="allocation", slot="spouse_fixed",
        conditions={"all": [RuleCondition(fact="exists", relation="Wife", operator="==", value=True), RuleCondition(fact="has_descendants", operator="==", value=False)]},
        actions=[RuleAction(type="assign_fraction", target="Wife", value="1/4", radd_eligible=False)],
        arabic_text="للزوجة الربع إذا لم يكن ولد", meaning="Wife receives 1/4 when no descendants exist"
    ),

    # --- LAYER 2: PARENTS ---
    Rule(
        rule_id="V7-PARENTS-ONLY", priority=700, category="allocation", slot="parents_fixed",
        conditions={
            "all": [
                RuleCondition(fact="count", relation="Father", operator="==", value=1),
                RuleCondition(fact="count", relation="Mother", operator="==", value=1),
                RuleCondition(fact="has_descendants", operator="==", value=False),
                RuleCondition(fact="total_valid_heirs", operator="==", value=2)
            ]
        },
        actions=[
            RuleAction(type="assign_fraction", target="Mother", value="1/3", radd_eligible=True),
            RuleAction(type="assign_fraction", target="Father", value="2/3", radd_eligible=True)
        ],
        arabic_text="فلأمه الثلث وللأب الثلثان", meaning="When only parents exist, Mother 1/3 and Father 2/3"
    ),
    Rule(
        rule_id="L2-MOTHER-CHILD", priority=710, category="allocation", slot="mother_fixed",
        conditions={"all": [RuleCondition(fact="exists", relation="Mother", operator="==", value=True), RuleCondition(fact="has_descendants", operator="==", value=True)]},
        actions=[RuleAction(type="assign_fraction", target="Mother", value="1/6", radd_eligible=True)],
        arabic_text="فللأم السدس مع الولد", meaning="Mother receives 1/6 when descendants exist"
    ),
    Rule(
        rule_id="L2-MOTHER-NO-CHILD", priority=720, category="allocation", slot="mother_fixed",
        conditions={"all": [RuleCondition(fact="exists", relation="Mother", operator="==", value=True), RuleCondition(fact="has_descendants", operator="==", value=False)]},
        actions=[RuleAction(type="assign_fraction", target="Mother", value="1/3", radd_eligible=True)],
        arabic_text="فللأم الثلث إذا لم يكن ولد", meaning="Mother receives 1/3 when no descendants exist"
    ),
    Rule(
        rule_id="L2-FATHER-CHILD", priority=730, category="allocation", slot="father_fixed",
        conditions={"all": [RuleCondition(fact="exists", relation="Father", operator="==", value=True), RuleCondition(fact="has_descendants", operator="==", value=True)]},
        actions=[RuleAction(type="assign_fraction", target="Father", value="1/6", radd_eligible=True)],
        arabic_text="للأب السدس مع الولد", meaning="Father receives 1/6 fixed when descendants exist"
    ),
    Rule(
        rule_id="L2-FATHER-REMAINDER", priority=740, category="allocation", slot="father_fixed",
        conditions={"all": [RuleCondition(fact="exists", relation="Father", operator="==", value=True)]},
        actions=[RuleAction(type="assign_remainder", target="Father")],
        arabic_text="والأب أقرب فيأخذ ما بقي", meaning="Father receives remainder when he exists"
    ),

    # --- LAYER 3: CLASS 2 (SIBLINGS) ---
    Rule(
        rule_id="L3-SIBLINGS-BLOCK", priority=1000, category="exclusion",
        conditions={"any": [RuleCondition(fact="exists", relation="Father", operator="==", value=True), RuleCondition(fact="has_descendants", operator="==", value=True)]},
        actions=[RuleAction(type="exclude_heir", target="Brother"), RuleAction(type="exclude_heir", target="Sister"), RuleAction(type="exclude_heir", target="Nephew")],
        arabic_text="ولا ميراث للإخوة مع الأب ولا مع الولد", meaning="Siblings blocked by Father or descendants"
    ),
    Rule(
        rule_id="L3-SIBLINGS-ALLOC", priority=1100, category="allocation", slot="class2_fixed",
        conditions={
            "all": [
                RuleCondition(fact="exists_class", target_class="siblings", operator="==", value=True),
                RuleCondition(fact="exists", relation="Father", operator="==", value=False),
                RuleCondition(fact="has_descendants", operator="==", value=False)
            ]
        },
        actions=[RuleAction(type="assign_remainder", target="Siblings")],
        arabic_text="فالميراث للإخوة", meaning="Siblings inherit remainder if Class 1 absent"
    ),

    # --- LAYER 3: CLASS 3 (UNCLES/COUSINS) ---
    Rule(
        rule_id="L3-UNCLES-BLOCK", priority=2000, category="exclusion",
        conditions={
            "any": [
                RuleCondition(fact="exists", relation="Father", operator="==", value=True),
                RuleCondition(fact="has_descendants", operator="==", value=True),
                RuleCondition(fact="exists", relation="Brother", operator="==", value=True),
                RuleCondition(fact="exists", relation="Sister", operator="==", value=True)
            ]
        },
        actions=[RuleAction(type="exclude_heir", target="Uncle"), RuleAction(type="exclude_heir", target="Cousin")],
        arabic_text="الأقرب يمنع الأبعد", meaning="Uncles blocked by Class 1 or Class 2"
    ),
    Rule(
        rule_id="L3-UNCLES-ALLOC", priority=2100, category="allocation", slot="class3_fixed",
        conditions={"all": [RuleCondition(fact="exists", relation="Uncle", operator="==", value=True)]},
        actions=[RuleAction(type="assign_remainder", target="Uncle")],
        arabic_text="فالميراث للأعمام", meaning="Uncles inherit remainder if closer kin absent"
    ),
    Rule(
        rule_id="L3-COUSINS-ALLOC", priority=2200, category="allocation", slot="class3_fixed",
        conditions={"all": [RuleCondition(fact="exists", relation="Cousin", operator="==", value=True)]},
        actions=[RuleAction(type="assign_remainder", target="Cousin")],
        arabic_text="فالميراث لبني الأعمام", meaning="Cousins inherit if no uncles exist"
    ),

    # --- FINAL: BAYT AL MAL ---
    Rule(
        rule_id="S9-BAYT-MAL", priority=9999, category="final",
        conditions={"all": [RuleCondition(fact="total_valid_heirs", operator="==", value=0)]},
        actions=[RuleAction(type="assign_remainder", target="Bayt_al_Mal")],
        arabic_text="بيت المال", meaning="Estate goes to Bayt al-Mal if no heirs exist"
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
        rel = condition.relation
        
        def get_count(relation_name):
            cnt = sum(h.count for h in self.state.valid_heirs if h.relation == relation_name)
            for src, as_rel in self.state.virtual_mappings.items():
                if as_rel == relation_name:
                    cnt += sum(h.count for h in self.state.valid_heirs if h.relation == src)
            return cnt

        if fact == "count":
            return get_count(rel)
        if fact == "exists":
            return get_count(rel) > 0
        if fact == "is_killer":
            return any(h.is_killer for h in self.state.heirs)
        if fact == "is_different_religion":
            return any(h.is_different_religion for h in self.state.heirs)
        if fact == "has_debts":
            return self.state.debts > 0
        if fact == "has_wasiyyah":
            return self.state.wasiyyah > 0
        if fact == "has_descendants":
            return any(get_count(r) > 0 for r in ["Son", "Daughter", "Grandson", "Granddaughter"])
        if fact == "total_heirs":
            return len(self.state.heirs)
        if fact == "total_valid_heirs":
            valid_non_excluded = [h for h in self.state.valid_heirs if h.relation not in self.state.excluded_relations]
            return len(valid_non_excluded)
        if fact == "exists_class":
            if condition.target_class == "siblings":
                return any(get_count(r) > 0 for r in ["Brother", "Sister"])
        return None

    def evaluate_rule(self, rule: Rule) -> bool:
        if rule.slot and rule.slot in self.state.occupied_slots:
            return False

        results = []
        for logic_type, conditions in rule.conditions.items():
            current_results = []
            for cond in conditions:
                fact_val = self._get_fact_value(cond)
                current_results.append(self.operators[cond.operator](fact_val, cond.value))
            
            if logic_type == "all":
                results.append(all(current_results))
            elif logic_type == "any":
                results.append(any(current_results))
            elif logic_type == "none":
                results.append(not any(current_results))
        
        return all(results) if results else False

    def fire_rule(self, rule: Rule):
        for action in rule.actions:
            if action.type == "procedure_action":
                if action.value == "subtract_debts":
                    self.state.estate_total -= self.state.debts
                elif action.value == "apply_wasiyyah_cap":
                    cap = self.state.estate_total / 3
                    self.state.estate_total -= min(self.state.wasiyyah, cap)
            elif action.type == "substitute_relation":
                self.state.virtual_mappings[action.source] = action.as_relation
            elif action.type == "exclude_heir":
                self.state.excluded_relations.add(action.target)
            elif action.type == "assign_fraction":
                self.state.assigned_fractions[action.target] = Fraction(action.value)
                if action.radd_eligible:
                    self.state.radd_pool.add(action.target)
            elif action.type == "assign_remainder":
                self.state.remainder_sink = action.target
        
        if rule.slot:
            self.state.occupied_slots.add(rule.slot)
        self.state.fired_rules.append(rule.rule_id)

class MathEngine:
    @staticmethod
    def resolve(state: CaseState) -> Dict[str, Any]:
        # 1. Remainder
        fixed_sum = sum(state.assigned_fractions.values())
        rem = Fraction(1, 1) - fixed_sum
        ledger = state.assigned_fractions.copy()

        if rem > 0:
            if state.remainder_sink:
                ledger[state.remainder_sink] = ledger.get(state.remainder_sink, Fraction(0)) + rem
            elif state.radd_pool:
                radd_sum = sum(ledger[r] for r in state.radd_pool if r in ledger)
                if radd_sum > 0:
                    for r in state.radd_pool:
                        if r in ledger:
                            ledger[r] += rem * (ledger[r] / radd_sum)
            else:
                ledger["Bayt_al_Mal"] = rem

        # 2. Expand into Individuals and Sort
        individual_results = []
        RELATION_ORDER = ["Father", "Mother", "Husband", "Wife", "Son", "Daughter", "Grandson", "Granddaughter", "Brother", "Sister", "Uncle", "Cousin", "Dhawu_Arham", "Bayt_al_Mal"]
        sorted_valid_heirs = sorted(state.valid_heirs, key=lambda h: RELATION_ORDER.index(h.relation) if h.relation in RELATION_ORDER else 99)

        applied_arabic = []
        for rid in state.fired_rules:
            rule_obj = next((r for r in KNOWLEDGE_BASE if r.rule_id == rid), None)
            if rule_obj: applied_arabic.append(rule_obj.arabic_text)

        for h in sorted_valid_heirs:
            if h.relation in state.excluded_relations: 
                continue
            effective_rel = state.virtual_mappings.get(h.relation, h.relation)
            share_val_for_relation_block = Fraction(0)
            
            if effective_rel in ledger:
                share_val_for_relation_block = ledger[effective_rel]
            elif effective_rel in ["Son", "Daughter"] and "Children" in ledger:
                def count_class(relation_name):
                    cnt = sum(x.count for x in state.valid_heirs if x.relation == relation_name and x.relation not in state.excluded_relations)
                    for src, as_rel in state.virtual_mappings.items():
                        if as_rel == relation_name:
                            cnt += sum(x.count for x in state.valid_heirs if x.relation == src and x.relation not in state.excluded_relations)
                    return cnt
                sons = count_class("Son")
                daughters = count_class("Daughter")
                units = (sons * 2) + daughters
                individual_unit = ledger["Children"] / units
                share_val_for_relation_block = (individual_unit * (2 if effective_rel == "Son" else 1)) * h.count
            elif effective_rel in ["Brother", "Sister"] and "Siblings" in ledger:
                bros = sum(x.count for x in state.valid_heirs if x.relation == "Brother")
                sis = sum(x.count for x in state.valid_heirs if x.relation == "Sister")
                units = (bros * 2) + sis
                individual_unit = ledger["Siblings"] / units
                share_val_for_relation_block = (individual_unit * (2 if effective_rel == "Brother" else 1)) * h.count

            if share_val_for_relation_block > 0:
                individual_share = share_val_for_relation_block / h.count
                for i in range(1, h.count + 1):
                    amt = individual_share * state.estate_total
                    individual_results.append(IndividualHeir(
                        heir_id=f"{h.relation}_{i}", relation=h.relation,
                        fraction=individual_share, amount=amt
                    ))

        if not individual_results and "Bayt_al_Mal" in ledger:
            amt = ledger["Bayt_al_Mal"] * state.estate_total
            individual_results.append(IndividualHeir(
                heir_id="Bayt_al_Mal_1", relation="Bayt_al_Mal",
                fraction=ledger["Bayt_al_Mal"], amount=amt
            ))
        elif "Bayt_al_Mal" in ledger and ledger["Bayt_al_Mal"] > 0:
            # If there are heirs but still a remainder for Bayt al Mal
            amt = ledger["Bayt_al_Mal"] * state.estate_total
            individual_results.append(IndividualHeir(
                heir_id="Bayt_al_Mal_1", relation="Bayt_al_Mal",
                fraction=ledger["Bayt_al_Mal"], amount=amt
            ))

        total_fraction = sum(h.fraction for h in individual_results)
        total_distributed = sum(h.amount for h in individual_results)
        is_valid = (total_fraction == Fraction(1, 1)) and (total_distributed == state.estate_total)
        
        if len(individual_results) > 0 and total_fraction != Fraction(1, 1):
            raise ValueError(f"Integrity check failed: Fraction sum is {total_fraction}")

        verification = VerificationData(
            estate_total=float(state.estate_total),
            total_distributed=float(total_distributed),
            fraction_sum=str(total_fraction),
            status="VALID" if is_valid else "INVALID"
        )

        final_results = [
            CalculationResult(
                heir_id=ir.heir_id, relation=ir.relation,
                share=str(ir.fraction.limit_denominator()),
                amount=round(float(ir.amount), 2),
                rules_used=state.fired_rules, arabic_reasoning=applied_arabic
            ) for ir in individual_results
        ]

        return {"results": final_results, "verification": verification}

class EnginePipeline:
    def calculate(self, heirs: List[Heir], estate_value: float, debts: float = 0.0, wasiyyah: float = 0.0) -> Dict[str, Any]:
        state = CaseState(estate_total=Fraction(estate_value), debts=Fraction(debts), wasiyyah=Fraction(wasiyyah), heirs=heirs)
        state.valid_heirs = [h for h in heirs if not (h.is_killer or h.is_different_religion)]
        engine = InferenceEngine(state)
        sorted_rules = sorted(KNOWLEDGE_BASE, key=lambda x: x.priority)
        for rule in sorted_rules:
            if engine.evaluate_rule(rule): engine.fire_rule(rule)
        return MathEngine.resolve(state)
