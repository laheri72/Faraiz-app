## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.

## 2024-06-05 - Memoizing derived chart data in interactive components
**Learning:** In components with interactive states (like mouse hover tracking), complex data derivations such as filtering, reducing, or building SVG slice arrays inside the render function will recalculate on every tick of the interactive state (e.g. mouse movement), causing severe recalculation overhead and UI jitter.
**Action:** Use `useMemo` to cache the derived data structures that depend only on static props (e.g. `results`) to decouple them from the interactive state updates.
