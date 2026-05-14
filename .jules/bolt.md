## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.
## 2024-05-13 - Component Hover State Recalculation
**Learning:** Derived data sets and complex calculations (like array filtering/reducing or chart mapping using `buildSlices`) in frontend React application require `useMemo` caching when used inside components with interactive states (e.g., hover events). Without `useMemo`, triggering these events causes severe recalculation overhead and UI jitter.
**Action:** Wrapped `activeResults`, `blockedResults`, `totalAmount`, and `slices` in a `useMemo` hook inside `DistributionPieChart.tsx` to depend only on `results`, avoiding recalculations on `hovered` state changes.
