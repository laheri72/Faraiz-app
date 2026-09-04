## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.
## 2024-05-14 - Closure reallocation overhead in hot loops
**Learning:** Defining inner functions within frequently called methods (hot loops), like `_get_fact_value` in the inheritance engine which is called thousands of times per request, incurs continuous closure reallocation overhead. This creates unnecessary work for the garbage collector and slows down the critical path.
**Action:** Extracted inner functions (`get_count`, `get_count_raw`, `add_rule_to_target`, `propagate_pool_rules`) to instance or module-level static methods and aliased them where appropriate to preserve performance while removing closure reallocation overhead.
