## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.

## 2024-05-18 - React useMemo for derived datasets in interactive components
**Learning:** In interactive components like charts, computing derived datasets (e.g. mapping and filtering arrays, reducing totals) inside the render block without memoization causes severe UI jitter and CPU overhead on frequent events like hover or mouse move.
**Action:** Use `useMemo` to cache these derived datasets so they only recalculate when their dependencies change, not on every local state update (like hover changes).
