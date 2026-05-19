## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.

## 2024-05-14 - Prevent UI jitter during hover interactions with useMemo
**Learning:** In React charts (like `DistributionPieChart`), filtering and mapping data (e.g. `results.filter` or `buildSlices`) on every render can cause severe overhead when interactive states (like `hovered`) change rapidly. This lack of memoization for complex derived data sets causes unnecessary recalculations and noticeable UI jitter.
**Action:** When implementing charts or lists with local interactive states, wrap derived data derivations (e.g., filtering, reducing, mapping) in `useMemo` hooks dependent on the primary data props to cache the calculation results.
