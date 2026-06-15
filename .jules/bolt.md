## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.


## 2024-05-20 - Dynamic Cache State vs Repeated Loops
**Learning:** Caching dynamic engine state (like `state.valid_heirs`) inside an initialization logic (`InferenceEngine.__init__`) is an anti-pattern when facts are updated dynamically. While trying to optimize O(N) list traversals into O(1) lookups, the engine failed because it was resolving based on stale data.
**Action:** Reverted state caching in InferenceEngine and optimized `KNOWLEDGE_BASE` evaluations which are static structure by pre-sorting it once at module level into `KNOWLEDGE_BASE_SORTED` rather than sorting it repetitively in loop.
