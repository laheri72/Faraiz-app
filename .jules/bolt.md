## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.

## 2024-05-07 - InferenceEngine Fact Gathering O(1) Cache
**Learning:** Replacing repeated linear list scans (O(n)) inside deeply-looped rule evaluation engines with a static hash map cache (O(1)) improves iteration performance significantly, provided the cache is scoped strictly to the evaluation engine (e.g. `InferenceEngine.__init__`) and not directly added to strict Pydantic model state. Dynamic conditions like excluded_relations must still be evaluated against the static cache at runtime.
**Action:** Applied a static dictionary map cache inside InferenceEngine for `get_count` and `get_count_raw`, which reduced inference iteration time from ~7s to ~5.5s over 5k loops.
