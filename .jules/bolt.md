## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.
## 2026-06-26 - O(N) evaluation logic in the Inference Engine
**Learning:** The rule engine (`InferenceEngine._get_fact_value`) was evaluating counts by repeatedly iterating over `self.state.valid_heirs` via list comprehensions for every condition check, leading to significant performance degradation (O(N) operation inside the evaluation loop).
**Action:** Precompute these static inputs in the engine's `__init__` into O(1) hash maps (`_raw_counts` and `_valid_heirs_by_rel`). Ensure dynamic states (like `self.state.excluded_relations`) are still evaluated against these precomputed caches at runtime.
