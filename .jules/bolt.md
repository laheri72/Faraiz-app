## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.

## 2024-07-05 - Avoid O(N) linear scans during fact gathering
**Learning:** The inheritance engine calculates states inside multiple nested loops, evaluating a static set of rules repeatedly. Relying on list comprehensions to count active heirs (`sum(h.count for h in self.state.valid_heirs)`) causes an O(N) scan inside `_get_fact_value()`, significantly hurting performance.
**Action:** Introduced an O(1) hash map cache (`_raw_counts`) populated once at the start of `InferenceEngine.__init__`. Dynamic conditions like `excluded_relations` are evaluated against these static counts at runtime, ensuring speed while maintaining correctness.
