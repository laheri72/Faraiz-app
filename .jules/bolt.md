## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.


## 2026-07-06 - O(1) hash map cache for runtime properties
**Learning:** During backend inference loops (e.g. `_get_fact_value`), linearly scanning `state.valid_heirs` inside frequently-called nested condition checks causes a repetitive O(N) penalty per rule evaluation. Pre-calculating these static sums once per class initialization and using a dictionary lookup dramatically improves calculation speed.
**Action:** Implemented `_raw_counts` hash map cache in `InferenceEngine.__init__` to avoid O(N) array scans during engine inference, allowing `get_count` and `get_count_raw` to return values in O(1) time.
