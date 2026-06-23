## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.

## 2024-05-18 - Pre-sort static rule sets to avoid loop overhead
**Learning:** In `backend/app/engine/core.py`, the `KNOWLEDGE_BASE` array was being dynamically sorted by priority on every single rule evaluation loop pass, creating significant CPU overhead (`O(N log N)` multiple times per calculation). Because `KNOWLEDGE_BASE` is a static list of rules, sorting it dynamically is unnecessary.
**Action:** Created a module-level `KNOWLEDGE_BASE_SORTED` that pre-sorts the rules once at import time, preventing redundant sorting during each request's engine calculation cycle.
