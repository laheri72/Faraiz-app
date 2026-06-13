## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.

## 2026-06-13 - Static metadata redundant sorting overhead
**Learning:** In the backend `EnginePipeline`, static rule metadata (`KNOWLEDGE_BASE`) was being re-sorted multiple times per request execution loop, leading to redundant CPU overhead. Python's `sorted()` was being called on a static 38-item list in the inner loop of `calculate()`.
**Action:** Pre-sort static configuration arrays at the module level (`KNOWLEDGE_BASE_SORTED`) and use the pre-sorted list in execution loops.
