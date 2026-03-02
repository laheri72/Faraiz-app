from typing import List, Dict, Any
from .models import Heir, CaseState, Rule, CalculationResult
from .rules_registry import RulesRegistry
from .evaluator import RuleEvaluator
from .priority_resolver import PriorityResolver
from .layer_5_math import MathEngine

class EnginePipeline:
    def __init__(self):
        self.registry = RulesRegistry()

    def calculate(self, heirs: List[Heir], estate_value: float) -> List[Dict[str, Any]]:
        state = CaseState(heirs=heirs)
        
        # Phase 1: Pre-process (Eligibility/Blocking)
        state = PriorityResolver.resolve_blocking(state)
        
        # Load and group rules by their functional layer
        rules = self.registry.get_rules_by_priority()
        
        # Iteratively apply rules from Layer 4 -> 1 -> 2 -> 3
        # In this prototype, we'll process all matching rules.
        # Deterministic order is maintained by rule priority in rules.json.
        for rule in rules:
            # Skip if any relation targeted by rule is excluded
            target_relation = rule.conditions.get("target_relation")
            if target_relation and target_relation in state.excluded_heirs:
                continue
                
            if RuleEvaluator.evaluate(state, rule):
                RuleEvaluator.apply_action(state, rule)
        
        # Check if we have children but no explicit assignment yet
        # (V1 applies for multiple children and doesn't set a 'fraction' directly in RuleEvaluator)
        if any(h.relation in ["Son", "Daughter"] for h in state.heirs) and not any(rel in ["Son", "Daughter", "Children"] for rel in state.assignments):
            # Children take the whole remainder after fixed shares
            fixed_sum = sum(state.assignments.values())
            remainder = 1 - fixed_sum
            if remainder > 0:
                # Add a virtual assignment for Children
                state.assignments["Son"] = remainder # Son/Daughter share is unified in MathEngine for V1
                state.assignments["Daughter"] = remainder
                # If both exist, V1 rule applies the split ratio in MathEngine

        # Layer 5: Math Engine
        final_shares = MathEngine.resolve_fractions(state, estate_value)
        
        # Attach explanation and rules used
        for res in final_shares:
            res["rules_used"] = state.applied_rules
            res["arabic_reasoning"] = [
                self.registry.get_rule_by_id(rid).arabic_text 
                for rid in state.applied_rules 
                if rid in state.applied_rules
            ]

        return final_shares
