## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.

## 2026-06-24 - Redundant sorting of static arrays in tight loops
**Learning:** Sorting a static rule base (`KNOWLEDGE_BASE`) on every iteration of a calculation loop causes massive, unnecessary processing overhead since the items do not change during runtime.
**Action:** Pre-sort static constants like `KNOWLEDGE_BASE` at the module level as `KNOWLEDGE_BASE_SORTED` to prevent redundant computations inside repetitive logic flows.
