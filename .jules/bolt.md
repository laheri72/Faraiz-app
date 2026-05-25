## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.
## 2024-05-25 - React useMemo optimization in interactive SVGs
**Learning:** In React components dealing with interactive SVGs (like `DistributionPieChart`), local state changes for hover events cause the entire component to re-render. If data processing or chart slice calculations are not memoized, these frequent hover events lead to severe recalculation overhead and UI jitter.
**Action:** Always wrap derived data calculations and complex view transformations (like `buildSlices`) in `useMemo` when a component handles frequent local state changes (e.g. mouse hover).
