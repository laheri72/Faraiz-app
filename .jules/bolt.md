## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.

## 2024-05-06 - useMemo requirement for heavy derived data in interactive components
**Learning:** Components that compute derived data sets (like `DistributionPieChart.tsx` mapping chart slices and reducing totals) and also have frequent interactive state updates (like `hovered` state driven by mouse events) MUST wrap the derived calculations in `useMemo`. Without it, every hover event triggers a full recalculation of the data, leading to significant UI jitter and main thread blocking, particularly with complex SVG rendering.
**Action:** Wrapped array filtering, reduction, and mapping in `DistributionPieChart.tsx` inside a `useMemo` dependency array tracking the `results` prop.
