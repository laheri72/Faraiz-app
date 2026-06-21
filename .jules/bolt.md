## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.
## 2026-06-21 - Optimize Knowledge Base Sorting in Inheritance Engine
**Learning:** In `backend/app/engine/core.py`, the static list `KNOWLEDGE_BASE` was being dynamically sorted on every loop iteration inside the core engine loop (`for rule in sorted(KNOWLEDGE_BASE, key=lambda x: x.priority):`). Since the knowledge base is static, sorting it repeatedly per case processing was unnecessary overhead.
**Action:** Created `KNOWLEDGE_BASE_SORTED` at the module level and updated the engine loop to iterate over it directly, reducing calculation time.
