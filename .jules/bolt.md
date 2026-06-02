## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.

## 2024-06-01 - Derived data calculations in interactive components
**Learning:** Components with local state tied to high-frequency events (like `onMouseEnter`/`onMouseLeave` hover states in charts) will trigger re-renders very frequently. If complex derived data (like filtering arrays or computing geometric slices) is calculated directly in the render body, it causes severe recalculation overhead and UI jitter.
**Action:** Always wrap heavy data transformations (`filter`, `reduce`, `map`) in `useMemo` when they rely on props in components that contain active interaction state.
