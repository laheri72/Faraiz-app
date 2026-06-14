## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.

## 2024-05-06 - Pre-sorting rules and pre-computing sum iterations
**Learning:** In the `InferenceEngine` inside `backend/app/engine/core.py`, sorting the static `KNOWLEDGE_BASE` and computing `sum()` loops dynamically for each rule evaluation condition created measurable overhead due to the engine's `O(n * m)` rule evaluation paths.
**Action:** Created `KNOWLEDGE_BASE_SORTED` at the module level to sort once, and pre-computed a `self._counts` dictionary inside `InferenceEngine.__init__` mapping relation types to counts to replace `O(n)` generator scans with `O(1)` dict lookups.
