## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.
## 2025-05-11 - useMemo in frontend pie chart
**Learning:** Derived data sets and complex calculations (like array filtering/reducing or chart mapping) require 'useMemo' caching when used inside components with interactive states (e.g., hover events) to prevent severe recalculation overhead and UI jitter.
**Action:** Added `useMemo` for derived datasets in `frontend/src/components/DistributionPieChart.tsx` to stop recreating slice path variables and filtering results when `hovered` state changes.
