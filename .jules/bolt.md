## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.
## 2026-06-01 - Array Iterations on Hover States
**Learning:** Derived data computations in components that contain interactive state (like a hover state) cause significant UI overhead if not memoized, because the array iterations (filter/map/reduce) run on every interactive state change.
**Action:** Always wrap derived datasets in `useMemo` when the component tracks rapid interactive state like `hovered` or `cursorPosition`.
