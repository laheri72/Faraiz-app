## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.

## 2026-05-08 - Pie chart hover recalculation overhead
**Learning:** In React functional components with frequently updating state variables (like `hovered` inside a chart segment mouse event), unmemoized variables trigger heavy recalculation logic (e.g. math intensive filter, reduce, and angle math map) every single render frame causing significant UI jitter.
**Action:** Used `useMemo` specifically on computationally heavy intermediate arrays/numbers that only depend on the top-level dataset properties.
