## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.
## 2024-06-25 - Python continuous closure reallocation in hot loops
**Learning:** Inner functions defined inside heavily called methods (such as `_get_fact_value` in the inheritance inference engine, called continuously during rule evaluation loops) cause massive performance overhead due to continuous closure reallocation.
**Action:** Extracted inner functions to instance and class-level methods, which successfully dropped engine calculation time from ~4.5 seconds to ~1.6 seconds per 1000 executions.
