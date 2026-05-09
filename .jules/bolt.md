## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.
## 2024-05-18 - React useMemo for derived state in hover-heavy components
**Learning:** In components with frequent state updates triggered by UI interactions (like hovering over pie chart slices), derived data sets (e.g. array filtering, reducing, mapping) must be memoized using `useMemo`. Otherwise, these expensive calculations will run on every render frame, causing noticeable UI jitter.
**Action:** When adding interactive state to a component, check if existing derived data needs to be wrapped in `useMemo`.
