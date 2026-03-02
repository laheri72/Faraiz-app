import json
import os
from typing import List
from .models import Rule

class RulesRegistry:
    def __init__(self, rules_path: str = None):
        if rules_path is None:
            # Assume rules.json is in the same directory as this file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            rules_path = os.path.join(current_dir, "rules.json")
        
        self.rules: List[Rule] = self._load_rules(rules_path)

    def _load_rules(self, path: str) -> List[Rule]:
        if not os.path.exists(path):
            return []
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Rule(**item) for item in data]

    def get_rules_by_priority(self) -> List[Rule]:
        return sorted(self.rules, key=lambda x: x.priority)

    def get_rule_by_id(self, rule_id: str) -> Rule:
        for rule in self.rules:
            if rule.rule_id == rule_id:
                return rule
        return None
