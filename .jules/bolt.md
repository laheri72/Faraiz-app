## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.

## 2024-05-06 - Python continuous closure reallocation overhead in hot loops
**Learning:** Defining inner functions (closures) inside a frequently executed method like `InferenceEngine._get_fact_value` causes Python to reallocate function objects on every single method call. In rule evaluation engines, where this method is called thousands of times per calculation loop, this creates continuous overhead (approx. 49% slower in microbenchmarks).
**Action:** Move inner functions out of the method body and turn them into class-level instance methods (e.g., `self._get_count`) so they are allocated only once.
