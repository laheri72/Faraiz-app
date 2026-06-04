## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.

## 2026-06-04 - Derived Data Performance Anti-Pattern in Interactive Charts
**Learning:** Derived data computations (like array filtering, mapping, and mathematical reduction) located at the top-level of a React functional component become severe performance bottlenecks when that component has frequent local state updates, such as hover events on a chart. In `DistributionPieChart.tsx`, iterating over `results` to compute `activeResults`, `blockedResults`, `totalAmount`, and `slices` re-ran on every mouse move.
**Action:** Always wrap expensive derived calculations inside a `useMemo` hook, especially when the component handles frequent interactive states like hovering.
