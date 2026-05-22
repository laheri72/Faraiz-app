## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.
## 2024-05-14 - Expensive derived calculations in UI with interactive states
**Learning:** Derived datasets and complex calculations (like array filtering/reducing or chart mapping) within a React component that also manages high-frequency interactive states (e.g., hover events) will recalculate on every single hover update, leading to severe UI jitter and calculation overhead.
**Action:** Always wrap heavy data processing blocks in `useMemo` when they rely on static props (like `results`) to ensure they are cached and skip recalculation during purely interactive state changes.
