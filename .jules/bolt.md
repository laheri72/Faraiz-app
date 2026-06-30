## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.

## 2024-05-14 - O(1) hash map cache pattern for fact gathering
**Learning:** `InferenceEngine._get_fact_value()` previously used O(N) linear scans (`sum(...)`) over `state.valid_heirs` for every rule condition evaluation. Since the total counts by relation type don't change dynamically within a case execution, precomputing an O(1) dictionary (`_raw_counts`) during `InferenceEngine.__init__` dramatically improves rule evaluation performance.
**Action:** Implemented `_raw_counts` hash map cache in `InferenceEngine.__init__`. Remember to evaluate dynamic state (like `excluded_relations`) against static caches at runtime, avoiding caching the dynamic values directly.
