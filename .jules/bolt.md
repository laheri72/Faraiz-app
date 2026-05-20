## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.

## 2024-05-07 - React missing useMemo in high-frequency interactive charts
**Learning:** In frontend chart components (e.g. `DistributionPieChart`) that handle rapid interactive state updates (like mouse hover `setHovered`), failing to wrap derived datasets in `useMemo` forces full recalculations and array instantiations (via `filter`, `reduce`, `map`) on every single hover event, causing measurable UI jitter and performance overhead.
**Action:** Always use `useMemo` to cache expensive derivations (e.g., `activeResults`, `blockedResults`, `totalAmount`, and `slices`) in components with high-frequency state updates, ensuring the dependencies (e.g., `results`) are explicitly provided.
