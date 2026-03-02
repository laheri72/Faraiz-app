from typing import Any, Dict, List, Optional
from fractions import Fraction
from .models import CaseState, Rule, Heir

class RuleEvaluator:
    @staticmethod
    def evaluate(state: CaseState, rule: Rule) -> bool:
        """
        Checks if the rule conditions are met for the current state.
        """
        conditions = rule.conditions
        
        # Check target_group conditions
        target_group = conditions.get("target_group")
        if target_group == "children":
            children = [h for h in state.heirs if h.relation in ["Son", "Daughter"]]
            if not children:
                return False
            
            # Check has_male/has_female
            if "has_male" in conditions and (any(c.relation == "Son" for c in children) != conditions["has_male"]):
                return False
            if "has_female" in conditions and (any(c.relation == "Daughter" for c in children) != conditions["has_female"]):
                return False
            
            # Check counts
            if "count" in conditions:
                for rel, req_count in conditions["count"].items():
                    actual_count = sum(c.count for c in children if c.relation.lower() == rel.lower())
                    if actual_count != req_count:
                        return False
        
        # Check target_relation conditions
        target_relation = conditions.get("target_relation")
        if target_relation:
            if target_relation == "Parents":
                 if not any(h.relation in ["Father", "Mother"] for h in state.heirs):
                     return False
                 # If it checks for children too
                 if "has_children" in conditions:
                     children_exist = any(h.relation in ["Son", "Daughter"] for h in state.heirs)
                     if children_exist != conditions["has_children"]:
                         return False
                 return True

            heir_found = next((h for h in state.heirs if h.relation == target_relation), None)
            if not heir_found:
                # Siblings might mean Brother OR Sister
                if target_relation == "Siblings":
                    if not any(h.relation in ["Brother", "Sister"] for h in state.heirs):
                        return False
                else:
                    return False
            
            if "has_children" in conditions:
                children_exist = any(h.relation in ["Son", "Daughter"] for h in state.heirs)
                if children_exist != conditions["has_children"]:
                    return False
            
            if "blocking_factors" in conditions:
                for factor in conditions["blocking_factors"]:
                    if factor == "Father" and any(h.relation == "Father" for h in state.heirs):
                        return True # Condition matches (heir is blocked)
                    if factor == "Children" and any(h.relation in ["Son", "Daughter"] for h in state.heirs):
                        return True
        
        return True

    @staticmethod
    def apply_action(state: CaseState, rule: Rule):
        """
        Applies rule actions to the state.
        """
        actions = rule.actions
        target_group = rule.conditions.get("target_group")
        target_relation = rule.conditions.get("target_relation")
        
        # assign_fraction
        if "assign_fraction" in actions:
            fraction = Fraction(actions["assign_fraction"])
            if actions.get("target_specific"):
                state.assignments[actions["target_specific"]] = fraction
            elif target_group == "children":
                # ... rest
                # Apply to specific child if it's "single daughter" etc.
                if "count" in rule.conditions:
                    for rel in rule.conditions["count"]:
                        rel_name = rel.capitalize()
                        state.assignments[rel_name] = fraction
                else:
                    # Generic children assignment (rare, usually ratio)
                    state.assignments["Children"] = fraction
            elif target_relation:
                state.assignments[target_relation] = fraction
        
        # assign_remainder
        if actions.get("assign_remainder"):
             if target_relation == "Father":
                 fixed_sum = sum(state.assignments.values())
                 state.assignments["Father"] = 1 - fixed_sum
        
        # Special case for V7 (Mother 1/3, Father 2/3)
        if rule.rule_id == "V7":
             state.assignments["Father"] = Fraction(2, 3)
             state.assignments["Mother"] = Fraction(1, 3)
        if actions.get("flag_radd"):
            if target_relation:
                state.radd_eligible.append(target_relation)
            elif target_group == "children":
                # Find which child to flag
                for h in state.heirs:
                    if h.relation in ["Son", "Daughter"]:
                        state.radd_eligible.append(h.relation)

        # block_relation
        if actions.get("block_relation"):
            if target_relation == "Siblings":
                for rel in ["Brother", "Sister"]:
                    if rel not in state.excluded_heirs:
                        state.excluded_heirs.append(rel)
            elif target_relation:
                if target_relation not in state.excluded_heirs:
                    state.excluded_heirs.append(target_relation)

        # apply_ratio (for V1, V15)
        if "apply_ratio" in actions:
            # Ratio is handled later by Math Engine, but we mark the heirs
            # For now, we'll store the ratio intent
            state.applied_rules.append(rule.rule_id)
            return

        state.applied_rules.append(rule.rule_id)
