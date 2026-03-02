import math
from typing import List, Dict, Any, Optional
from fractions import Fraction
from .models import Heir, CaseState, Rule

# Rule Definitions (In-memory registry for v2)
V2_RULES = {
    "S1-KILLER": Rule(rule_id="S1-KILLER", arabic_text="القاتل لا يرث", meaning="Killer does not inherit"),
    "S2-RELIGION": Rule(rule_id="S2-RELIGION", arabic_text="اختلاف الدين يمنع الميراث", meaning="Religion difference blocks inheritance"),
    "S5-DEBT": Rule(rule_id="S5-DEBT", arabic_text="الدين قبل الوصية والميراث", meaning="Debts paid first"),
    "S6-WASIYYAH": Rule(rule_id="S6-WASIYYAH", arabic_text="الوصية في الثلث", meaning="Wasiyyah limited to 1/3"),
    "F1-SON-DAUGHTER": Rule(rule_id="F1-SON-DAUGHTER", arabic_text="للذكر مثل حظ الأنثيين", meaning="Male gets double female"),
    "F2-SINGLE-SON": Rule(rule_id="F2-SINGLE-SON", arabic_text="فإن لم يترك غير ولد واحد ذكر فالميراث له كله", meaning="Single son receives 100%"),
    "F3-SINGLE-DAUGHTER": Rule(rule_id="F3-SINGLE-DAUGHTER", arabic_text="فللابنة النصف بالميراث المسمى ويرد عليها", meaning="Single daughter gets 1/2 fixed, 1/2 radd"),
    "F4-TWO-DAUGHTERS": Rule(rule_id="F4-TWO-DAUGHTERS", arabic_text="فلكل واحدة الثلث بالميراث ويرد عليهما", meaning="Two daughters each get 1/3 fixed, remainder radd"),
    "F8-PARENTS-ONLY": Rule(rule_id="F8-PARENTS-ONLY", arabic_text="فلأمه الثلث وللأب الثلثان", meaning="Mother 1/3, Father 2/3"),
    "L2-HUSBAND": Rule(rule_id="L2-HUSBAND", arabic_text="للزوج النصف أو الربع", meaning="Husband gets 1/2 or 1/4"),
    "L2-WIFE": Rule(rule_id="L2-WIFE", arabic_text="للزوجة الربع أو الثمن", meaning="Wife gets 1/4 or 1/8"),
    "L2-MOTHER": Rule(rule_id="L2-MOTHER", arabic_text="للأم الثلث أو السدس", meaning="Mother gets 1/3 or 1/6"),
    "L2-FATHER": Rule(rule_id="L2-FATHER", arabic_text="للأب التعصيب مع الولد أو الثلثان", meaning="Father residuary or 2/3"),
    "L3-PRIORITY": Rule(rule_id="L3-PRIORITY", arabic_text="الأقرب يمنع الأبعد", meaning="Nearer relative blocks distant"),
    "L3-GRANDCHILDREN": Rule(rule_id="L3-GRANDCHILDREN", arabic_text="ولد الولد يقوم مقام الولد", meaning="Grandchildren substitute children"),
    "L3-SIBLINGS": Rule(rule_id="L3-SIBLINGS", arabic_text="ولا ميراث للإخوة مع الأب ولا مع الولد", meaning="Siblings blocked by Father/Children"),
    "L3-UNCLES": Rule(rule_id="L3-UNCLES", arabic_text="فالميراث للأعمام", meaning="Uncles inherit if no closer heirs"),
    "L3-COUSINS": Rule(rule_id="L3-COUSINS", arabic_text="فالميراث لبني الأعمام", meaning="Cousins inherit if no uncles"),
    "V27-DHAWU-ARHAM": Rule(rule_id="V27-DHAWU-ARHAM", arabic_text="فالميراث لذوي الأرحام", meaning="Dhawu al-Arham inherit if no others"),
    "S9-BAYT-MAL": Rule(rule_id="S9-BAYT-MAL", arabic_text="بيت المال", meaning="Bayt al-Mal if no heirs")
}

class Layer4_SpecialRules:
    """Layer 4: Eligibility & Exclusions. Runs FIRST."""
    @staticmethod
    def apply(state: CaseState) -> CaseState:
        # 1. Debts & Wasiyyah
        estate = state.estate_total
        if state.debts > 0:
            estate -= state.debts
            state.applied_rules.append("S5-DEBT")
            
        if state.wasiyyah > 0:
            max_wasiyyah = estate / 3
            wasiyyah_applied = min(state.wasiyyah, max_wasiyyah)
            estate -= wasiyyah_applied
            state.applied_rules.append("S6-WASIYYAH")
            
        state.estate_total = max(0, estate)
        
        # 2. Eligibility (Killer, Religion, Lineage, Missing)
        for heir in state.heirs:
            if heir.is_killer:
                state.applied_rules.append("S1-KILLER")
                continue
            if heir.is_different_religion:
                state.applied_rules.append("S2-RELIGION")
                continue
            if heir.is_missing:
                # simplify: held share or excluded
                continue
            state.valid_heirs.append(heir)
            
        return state

class Layer1_Children:
    """Layer 1: Direct descendant resolution."""
    @staticmethod
    def apply(state: CaseState):
        sons = [h for h in state.valid_heirs if h.relation == "Son"]
        daughters = [h for h in state.valid_heirs if h.relation == "Daughter"]
        
        num_sons = sum(s.count for s in sons)
        num_daughters = sum(d.count for d in daughters)
        
        if num_sons > 0 or num_daughters > 0:
            if num_sons == 1 and num_daughters == 0:
                state.assignments["Son"] = Fraction(1, 1) # Handled mathematically later
                state.applied_rules.append("F2-SINGLE-SON")
            elif num_sons == 0 and num_daughters == 1:
                state.assignments["Daughter"] = Fraction(1, 2)
                state.radd_eligible.append("Daughter")
                state.applied_rules.append("F3-SINGLE-DAUGHTER")
            elif num_sons == 0 and num_daughters == 2:
                state.assignments["Daughter"] = Fraction(2, 3)
                state.radd_eligible.append("Daughter")
                state.applied_rules.append("F4-TWO-DAUGHTERS")
            elif num_sons > 0 and num_daughters > 0:
                # Handled by ratio later
                state.applied_rules.append("F1-SON-DAUGHTER")
                state.assignments["Children"] = Fraction(1, 1) # Placeholder for MathEngine
            elif num_sons > 1 and num_daughters == 0:
                state.assignments["Son"] = Fraction(1, 1)

class Layer2_FixedShares:
    """Layer 2: Fixed Shares (Spouses, Parents)."""
    @staticmethod
    def apply(state: CaseState):
        heir_rels = [h.relation for h in state.valid_heirs]
        has_children = "Son" in heir_rels or "Daughter" in heir_rels
        has_grandchildren = "Grandson" in heir_rels or "Granddaughter" in heir_rels
        has_descendant = has_children or has_grandchildren

        for h in state.valid_heirs:
            if h.relation == "Husband":
                state.assignments["Husband"] = Fraction(1, 4) if has_descendant else Fraction(1, 2)
                state.applied_rules.append("L2-HUSBAND")
            elif h.relation == "Wife":
                state.assignments["Wife"] = Fraction(1, 8) if has_descendant else Fraction(1, 4)
                state.applied_rules.append("L2-WIFE")
            elif h.relation == "Mother":
                state.assignments["Mother"] = Fraction(1, 6) if has_descendant else Fraction(1, 3)
                state.radd_eligible.append("Mother")
                state.applied_rules.append("L2-MOTHER")

        # Father logic
        if "Father" in heir_rels:
            if not has_descendant:
                if "Mother" in heir_rels and len(state.valid_heirs) == 2:
                    # Parents only: F8
                    state.assignments["Mother"] = Fraction(1, 3)
                    state.assignments["Father"] = Fraction(2, 3)
                    state.applied_rules.append("F8-PARENTS-ONLY")
                else:
                    # Father gets remainder
                    state.assignments["Father"] = Fraction(1, 1) # Place holder for remainder
            state.applied_rules.append("L2-FATHER")
            
class Layer3_Priority:
    """Layer 3: Priority Engine (Kinship Distance Graph)."""
    @staticmethod
    def apply(state: CaseState):
        heir_rels = [h.relation for h in state.valid_heirs]
        
        has_children = "Son" in heir_rels or "Daughter" in heir_rels
        has_parents = "Father" in heir_rels or "Mother" in heir_rels # Father blocks siblings
        
        # If Children or Father exist, they block all extended relations
        if has_children or "Father" in heir_rels:
            state.applied_rules.append("L3-PRIORITY")
            return
            
        # Level 3: Grandchildren
        if "Grandson" in heir_rels or "Granddaughter" in heir_rels:
            state.applied_rules.append("L3-GRANDCHILDREN")
            state.assignments["Grandchildren"] = Fraction(1,1)
            return
            
        # Level 4: Siblings
        has_siblings = "Brother" in heir_rels or "Sister" in heir_rels
        if has_siblings:
            state.applied_rules.append("L3-SIBLINGS")
            state.assignments["Siblings"] = Fraction(1,1)
            return
            
        # Level 5: Nephews (Brother_Son etc - simplified as Nephew)
        if "Nephew" in heir_rels:
            state.assignments["Nephew"] = Fraction(1,1)
            return
            
        # Level 6: Uncles
        if "Uncle" in heir_rels:
            state.applied_rules.append("L3-UNCLES")
            state.assignments["Uncle"] = Fraction(1,1)
            return
            
        # Level 7: Cousins
        if "Cousin" in heir_rels:
            state.applied_rules.append("L3-COUSINS")
            state.assignments["Cousin"] = Fraction(1,1)
            return
            
        # Level 8: Dhawu al-Arham
        if "Dhawu_Arham" in heir_rels:
            state.applied_rules.append("V27-DHAWU-ARHAM")
            state.assignments["Dhawu_Arham"] = Fraction(1,1)
            return

        # Level 9: Bayt al-Mal
        state.applied_rules.append("S9-BAYT-MAL")
        state.assignments["Bayt_al_Mal"] = Fraction(1,1)


class Layer5_Math:
    """Layer 5: Mathematical Unification & LCM."""
    @staticmethod
    def get_lcm(numbers: List[int]) -> int:
        if not numbers: return 1
        lcm = numbers[0]
        for i in range(1, len(numbers)):
            lcm = abs(lcm * numbers[i]) // math.gcd(lcm, numbers[i])
        return lcm

    @staticmethod
    def apply(state: CaseState, original_estate: float) -> List[Dict[str, Any]]:
        # Calculate fixed shares
        fixed_sum = Fraction(0, 1)
        fixed_assignments = {}
        
        # Pull fixed shares out of assignments (ignoring remainder placeholders like 1/1 for Father/Children)
        remainder_keys = ["Son", "Children", "Father", "Grandchildren", "Siblings", "Nephew", "Uncle", "Cousin", "Dhawu_Arham", "Bayt_al_Mal"]
        
        for rel, frac in list(state.assignments.items()):
            if rel not in remainder_keys and rel != "Daughter": 
                fixed_sum += frac
                fixed_assignments[rel] = frac
            elif rel == "Daughter" and "F1-SON-DAUGHTER" not in state.applied_rules and "Son" not in [h.relation for h in state.valid_heirs]:
                fixed_sum += frac
                fixed_assignments[rel] = frac

        remainder = Fraction(1, 1) - fixed_sum

        # Distribute remainder / Radd
        if remainder > 0:
            active_remainder_heirs = [rel for rel in remainder_keys if rel in state.assignments]
            if active_remainder_heirs:
                # Group shares like "Children" or "Siblings"
                for rel in active_remainder_heirs:
                    fixed_assignments[rel] = remainder
            elif state.radd_eligible:
                # Radd proportional
                radd_sum = sum(fixed_assignments[r] for r in state.radd_eligible if r in fixed_assignments)
                if radd_sum > 0:
                    for r in state.radd_eligible:
                        if r in fixed_assignments:
                            fixed_assignments[r] += remainder * (fixed_assignments[r] / radd_sum)
            else:
                # No radd eligible, no remainder heirs -> Bayt al Mal
                fixed_assignments["Bayt_al_Mal"] = remainder

        # Ratio split logic (2:1 for male:female)
        final_results = []
        for h in state.valid_heirs:
            share_val = Fraction(0, 1)
            
            if h.relation in fixed_assignments:
                share_val = fixed_assignments[h.relation]
            elif h.relation in ["Son", "Daughter"] and "Children" in fixed_assignments:
                # F1 ratio
                sons = sum(s.count for s in state.valid_heirs if s.relation == "Son")
                daughters = sum(d.count for d in state.valid_heirs if d.relation == "Daughter")
                units = (sons * 2) + daughters
                group_share = fixed_assignments["Children"]
                if units > 0:
                    unit_share = group_share / units
                    share_val = (unit_share * 2) if h.relation == "Son" else unit_share
            elif h.relation in ["Grandson", "Granddaughter"] and "Grandchildren" in fixed_assignments:
                grandsons = sum(s.count for s in state.valid_heirs if s.relation == "Grandson")
                granddaughters = sum(d.count for d in state.valid_heirs if d.relation == "Granddaughter")
                units = (grandsons * 2) + granddaughters
                group_share = fixed_assignments["Grandchildren"]
                if units > 0:
                    unit_share = group_share / units
                    share_val = (unit_share * 2) if h.relation == "Grandson" else unit_share
            elif h.relation in ["Brother", "Sister"] and "Siblings" in fixed_assignments:
                brothers = sum(s.count for s in state.valid_heirs if s.relation == "Brother")
                sisters = sum(d.count for d in state.valid_heirs if d.relation == "Sister")
                units = (brothers * 2) + sisters
                group_share = fixed_assignments["Siblings"]
                if units > 0:
                    unit_share = group_share / units
                    share_val = (unit_share * 2) if h.relation == "Brother" else unit_share
            
            if share_val > 0:
                amt = float(share_val) * state.estate_total
                frac_str = str(share_val.limit_denominator())
                final_results.append({
                    "heir": h.relation,
                    "count": h.count,
                    "share": frac_str,
                    "amount": round(amt, 2)
                })
        
        # Include Bayt_al_Mal if present
        if "Bayt_al_Mal" in fixed_assignments and fixed_assignments["Bayt_al_Mal"] > 0:
            final_results.append({
                "heir": "Bayt_al_Mal",
                "count": 1,
                "share": str(fixed_assignments["Bayt_al_Mal"].limit_denominator()),
                "amount": round(float(fixed_assignments["Bayt_al_Mal"]) * state.estate_total, 2)
            })

        return final_results

class EnginePipeline:
    def calculate(self, heirs: List[Heir], estate_value: float, debts: float = 0.0, wasiyyah: float = 0.0) -> List[Dict[str, Any]]:
        state = CaseState(estate_total=estate_value, debts=debts, wasiyyah=wasiyyah, heirs=heirs)
        
        # Layer 4: Special Rules
        state = Layer4_SpecialRules.apply(state)
        
        # Layer 1: Children
        Layer1_Children.apply(state)
        
        # Layer 2: Fixed Shares
        Layer2_FixedShares.apply(state)
        
        # Layer 3: Priority / Proximity
        Layer3_Priority.apply(state)
        
        # Layer 5: Math Engine & Resolution
        results = Layer5_Math.apply(state, estate_value)
        
        # Attach reasoning
        applied_arabic = [V2_RULES[rid].arabic_text for rid in state.applied_rules if rid in V2_RULES]
        for r in results:
            r["rules_used"] = state.applied_rules
            r["arabic_reasoning"] = applied_arabic
            
        return results
