## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.

## 2026-05-21 - Derived React datasets and hover state performance
**Learning:** Performing complex data derivation (like array filtering/reducing or chart mapping calculations) synchronously during rendering is highly problematic if the component also maintains high-frequency interactive states (like hover events). Every hover change triggers a re-render, forcing a full recalculation of the heavy logic and causing noticeable UI jitter.
**Action:** Use `useMemo` with the actual data dependencies (e.g. `[results]`) for derived datasets in components with interactive states to prevent this severe recalculation overhead.
