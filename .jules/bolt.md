## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.

## 2024-07-04 - Cached heir counting to avoid O(N) lookup overhead in calculations
**Learning:** During rule evaluation, `InferenceEngine._get_fact_value()` repeatedly performed O(N) linear scans over `self.state.valid_heirs` within a list comprehension, which caused unnecessary overhead during fact gathering loops. Because the set of valid heirs remains static per inference layer, caching these counts into a dictionary upon initialization of `InferenceEngine` dramatically improves lookup performance to O(1).
**Action:** Implemented a `self._raw_counts` O(1) hash map initialized once in `InferenceEngine.__init__`. Dynamic state like exclusions is still evaluated against the cache, adhering to schema constraints without adding caching directly to Pydantic models.
