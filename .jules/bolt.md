## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.
## 2024-05-18 - Caching sorted static structures in inference engine
**Learning:** The Python backend was re-sorting `KNOWLEDGE_BASE` inside the `for _ in range(3):` loop on every calculate call. Since `KNOWLEDGE_BASE` is a static list of rules loaded at startup, it only needs to be sorted once.
**Action:** Created `KNOWLEDGE_BASE_SORTED` at the module level in `backend/app/engine/core.py` to prevent redundant sorting overhead on every calculation, speeding up the raw loop by ~10x.
