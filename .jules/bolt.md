## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.

## $(date +%Y-%m-%d) - Short-circuiting custom InferenceEngine condition evaluations
**Learning:** In the `InferenceEngine.evaluate_rule` loop, the conditions logic used list comprehensions (`[evaluate(c) for c in conditions]`) before calling `all()` or `any()`. This evaluated every condition fully, even if the first condition in an `all` logic failed, leading to unnecessary operations and loops inside `_get_fact_value`.
**Action:** Replaced the list comprehensions with generator expressions (`all(evaluate(c) for c in conditions)`) to allow short-circuiting. If `results` appends `False` and the rule is composed of an `all()` wrapper, you can also early return `False` directly from the loop.
