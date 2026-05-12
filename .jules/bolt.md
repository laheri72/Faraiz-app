## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.

## 2024-05-12 - Missing useMemo inside frequently updated interactive components
**Learning:** In the frontend React application, derived data sets and complex calculations (like array filtering/reducing or chart mapping) require `useMemo` caching when used inside components with interactive states (e.g., hover events). Without `useMemo`, these `O(n)` array operations are unnecessarily recalculated on every hover event, causing recalculation overhead and UI jitter.
**Action:** Wrapped derived data like `activeResults`, `blockedResults`, `totalAmount`, and `slices` inside `useMemo` hooks in `DistributionPieChart.tsx`.
