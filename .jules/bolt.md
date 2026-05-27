## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.

## 2024-05-24 - Expensive Data Transformation Overhead on Hover
**Learning:** Derived data sets and complex calculations (like `buildSlices` chart mapping) inside components with interactive states (like SVG slice hover events) cause severe UI jitter and recalculation overhead if not cached. Because `results` props are stable but `hovered` state changes frequently, lack of memoization recalculates everything on every mouse move.
**Action:** When a component has interactive visual states (e.g., hover tracking), always wrap expensive prop derivations (filtering, reducing, complex mapping) in `useMemo`.
