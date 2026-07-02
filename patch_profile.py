import re

with open('backend/app/engine/core.py', 'r') as f:
    content = f.read()

# Replace __init__ to add _raw_counts
content = content.replace(
"""class InferenceEngine:
    def __init__(self, state: CaseState):
        self.state = state
        self.operators = {
            "==": operator.eq, ">=": operator.ge, ">": operator.gt,
            "<": operator.lt, "<=": operator.le, "!=": operator.ne
        }""",
"""class InferenceEngine:
    def __init__(self, state: CaseState):
        self.state = state
        self.operators = {
            "==": operator.eq, ">=": operator.ge, ">": operator.gt,
            "<": operator.lt, "<=": operator.le, "!=": operator.ne
        }
        self._raw_counts = {}
        for h in state.valid_heirs:
            self._raw_counts[h.relation_type] = self._raw_counts.get(h.relation_type, 0) + h.count"""
)

# Replace get_count and get_count_raw
content = content.replace(
"""        def get_count(target_rel_type):
            return sum(h.count for h in self.state.valid_heirs if h.relation_type == target_rel_type and h.relation_type not in self.state.excluded_relations)

        def get_count_raw(target_rel_type):
            return sum(h.count for h in self.state.valid_heirs if h.relation_type == target_rel_type)""",
"""        def get_count(target_rel_type):
            if target_rel_type in self.state.excluded_relations:
                return 0
            return self._raw_counts.get(target_rel_type, 0)

        def get_count_raw(target_rel_type):
            return self._raw_counts.get(target_rel_type, 0)"""
)

with open('backend/app/engine/core.py', 'w') as f:
    f.write(content)
