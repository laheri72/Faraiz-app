## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.

## 2026-07-01 - Expensive static rule sorting and linear lookups during calculations
**Learning:** The inheritance engine repeatedly sorts the entire `KNOWLEDGE_BASE` and does linear O(N) list scans (using `next((r for r in KNOWLEDGE_BASE if ...))`) inside the calculation loop and resolution phase. This causes high CPU overhead per inheritance case.
**Action:** Defined `KNOWLEDGE_BASE_BY_ID` (hash map) and `KNOWLEDGE_BASE_SORTED` (list) globally at the module level. Replaced dynamic sorting with the pre-sorted list, and replaced O(N) linear scans with O(1) dictionary lookups.
