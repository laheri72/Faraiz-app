## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.
## 2024-05-07 - React useMemo necessity in interactive SVG charts
**Learning:** In frontend React applications, complex derived datasets (like SVG pie chart slices and aggregated totals) calculated directly in the component body will cause severe recalculation overhead and UI jitter if the component contains interactive state (like hover events on SVG elements).
**Action:** Added `useMemo` to `activeResults`, `blockedResults`, `totalAmount`, and `slices` in `DistributionPieChart` to cache these calculations, dependent only on the `results` prop, preventing recalculation during hover interactions.
