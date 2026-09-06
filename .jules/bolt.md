## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.
## 2024-05-18 - Python closure reallocation overhead in hot loops
**Learning:** Defining inner functions within frequently called methods (e.g. `def get_count` inside `_get_fact_value`, or `def add_rule_to_target` inside `fire_rule`) incurs continuous closure reallocation overhead. Moving these to instance methods provides measurable speedup for calculation-heavy endpoints (e.g., in a deterministic rules engine).
**Action:** Extracted inner functions in `core.py` hot loops (`_get_fact_value` and `fire_rule`) to instance methods (`_get_count` and `_add_rule_to_target`).
