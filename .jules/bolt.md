## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.

## 2024-05-18 - Python closure overhead in hot loops
**Learning:** In Python, defining inner functions within frequently called methods (hot loops, such as `_get_fact_value` evaluating facts across rules) incurs continuous closure reallocation overhead. Extracting these functions to instance methods (`_get_count` and `_get_count_raw`) avoids this overhead and provides measurable execution speedups.
**Action:** Extracted inner closures out of `_get_fact_value` and `fire_rule` to `InferenceEngine` instance methods to improve core engine rule evaluation performance.
