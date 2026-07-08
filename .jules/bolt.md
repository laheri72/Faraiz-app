## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.

## 2024-05-17 - O(N) array scans during nested rule evaluation
**Learning:** In rule engines that repeatedly evaluate conditions across many iterations, dynamically calculating counts of entities (e.g. `sum(h.count for h in valid_heirs if h.type == x)`) inside the condition-checking loop creates an O(N) bottleneck per condition per rule. Even if the array is small, the multiplier of `Rules × Iterations` makes it slow.
**Action:** Implemented a pre-computed O(1) hash map `_raw_counts` scoped to the engine instance. Dynamic exclusions (e.g., relations blocked during runtime) are checked against a separate O(1) set (`state.excluded_relations`) inside the getter instead of re-iterating over the original heir list.
