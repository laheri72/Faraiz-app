## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.

## 2024-05-28 - Missing useMemo causes UI jitter on hover interactions
**Learning:** In React components with interactive states (like `DistributionPieChart`'s hover state `hovered`), derived data structures like array filters/reduces and complex object mapping (`buildSlices`) must be cached with `useMemo`. If omitted, they re-evaluate on every tiny hover event, leading to severe recalculation overhead and UI jitter.
**Action:** Added `useMemo` for derived dataset arrays and aggregate variables in `DistributionPieChart.tsx`.
