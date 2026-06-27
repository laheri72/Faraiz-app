## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.
## 2025-02-18 - Inference Engine O(1) Cache Lookup Optimization
**Learning:** The Inference Engine evaluates conditions repeatedly during calculations. Previously, gathering heir counts involved an O(N) list comprehension over `state.valid_heirs` on every single check, causing massive redundant overhead.
**Action:** Replaced O(N) linear scans with O(1) lookups using an initialized `_raw_counts` dictionary cache within the `InferenceEngine` to retrieve counts efficiently.
