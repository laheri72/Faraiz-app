## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.

## 2024-06-18 - Pre-sorting static KNOWLEDGE_BASE for inference engine
**Learning:** Inheritance logic and static rule metadata for the engine (`KNOWLEDGE_BASE`) were being repeatedly sorted on every evaluation loop iteration, adding redundant overhead. Static rule arrays should be pre-sorted at the module level.
**Action:** Defined `KNOWLEDGE_BASE_SORTED` at the module level in `backend/app/engine/core.py` and replaced the dynamic `sorted()` call to avoid redundant sorting during calculation loops.
