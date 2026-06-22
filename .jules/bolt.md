## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.

## 2024-05-18 - Module-level sorting for static rules
**Learning:** Inheritance logic and static rule metadata for the engine (`KNOWLEDGE_BASE`) are defined directly as a static list. Sorting this list dynamically inside calculation loops using `sorted()` introduces unnecessary O(N log N) overhead on every calculation pass.
**Action:** Introduced `KNOWLEDGE_BASE_SORTED` at the module level to pre-sort the static list, removing redundant sorting overhead during calculation loop passes.
