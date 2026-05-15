## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.

## 2024-05-15 - Optimizing list lookups in loops with dictionaries
**Learning:** In inference engines or processing loops, finding items in an array/list using a linear search (e.g. `next(r for r in list if r.id == id, None)`) inside loops can add up to O(N * M) performance hits. Converting the static rule list into an O(1) module-level dictionary lookup (`{r.id: r for r in list}`) significantly speeds up the reasoning retrieval step without changing system architecture.
**Action:** Used a module-level `RULE_MAP` for `KNOWLEDGE_BASE` rules to make `rule_id` lookups O(1) inside `MathEngine.resolve` loops.
