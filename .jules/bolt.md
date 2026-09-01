## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.
## 2024-05-15 - Inner function allocation in hot paths
**Learning:** In Python, defining inner functions (like `get_count` inside `_get_fact_value`) incurs a measurable overhead if the outer function is called repeatedly in a hot loop (like rule evaluation during the engine's inference cycle). The closure is re-created on every call.
**Action:** Extract inner functions to instance or module-level methods when they are inside critical O(N^2) or highly iterative paths to avoid continuous reallocation overhead.
