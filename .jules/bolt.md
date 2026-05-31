## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.

## 2024-05-15 - Derived data caching with interactive state overhead
**Learning:** Derived data arrays and reduction logic in React components mapping complex visual elements (e.g., SVG slices in a PieChart) must be memoized when the component contains a local interactive state that updates frequently, such as a hover event index. Without `useMemo`, triggering hover states forces the entire component to re-execute data processing on each microscopic DOM event, causing severe UI lag.
**Action:** Wrapped derived data arrays (`activeResults`, `blockedResults`, `totalAmount`, `slices`) using `useMemo` with their base dependencies.
