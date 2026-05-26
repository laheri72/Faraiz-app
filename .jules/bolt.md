## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.

## 2026-05-26 - Expensive derived state in interactive components
**Learning:** Derived dataset calculations (like array filtering and reducing) and component-specific mapping logic (like pie chart slices) inside components with interactive states (e.g. hover events) cause significant recalculation overhead leading to performance degradation and UI jitter on every interaction.
**Action:** Use `useMemo` to wrap derived data calculation with proper dependency tracking to isolate and prevent expensive recalculations during unrelated state changes.
