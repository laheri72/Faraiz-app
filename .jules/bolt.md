## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.

## 2026-05-17 - Caching and O(1) lookups for static knowledge base
**Learning:** In `backend/app/engine/core.py`, linear list comprehensions and repetitive dynamic sorting over `KNOWLEDGE_BASE` can create unnecessary overhead during inheritance calculation loops. Because the rules are a static list, they can be indexed via a module-level dictionary mapping (`RULE_MAP`) and pre-sorted once (`SORTED_KNOWLEDGE_BASE`) for O(1) lookups and faster iteration without continuous recalculation.
**Action:** Replaced `next()` lookups and array iterations with a cached `RULE_MAP` and swapped `sorted(KNOWLEDGE_BASE)` for a module-level cached list. This dramatically avoids O(n) lookups during repeated pipeline runs.
