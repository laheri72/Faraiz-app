## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.

## 2024-05-07 - React useMemo necessity in interactive SVG charts
**Learning:** Derived data sets and complex calculations (like array filtering/reducing or chart mapping) require `useMemo` caching when used inside components with interactive states (e.g., hover events) to prevent severe recalculation overhead and UI jitter. In `DistributionPieChart`, the slices were being recalculated on every single mouse hover event.
**Action:** Wrapped derived data and chart slice building (`activeResults`, `blockedResults`, `totalAmount`, `slices`) in `useMemo` with `results` as the dependency to isolate expensive operations from fast-changing hover state.
