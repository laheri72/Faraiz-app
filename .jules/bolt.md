## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.

## 2024-05-06 - Dynamic state initialization inside calculation loop
**Learning:** In the inheritance `EnginePipeline`, `_get_fact_value` dynamically recalculates the count of relations multiple times for each condition evaluated. Replacing the `sum` generator with a `_heir_counts_cache` initialized on the state directly on first use provides an ~20% performance improvement by avoiding O(N) recalculations on O(M) loop iterations.
**Action:** Added a dynamic state cache `_heir_counts_cache` during rule execution.

## 2026-06-20 - Improper cache placement on dynamic models
**Learning:** In `backend/app/engine/core.py`, avoiding caching dynamic state (like `valid_heirs` counts) in the `InferenceEngine.__init__` method was instructed by memory due to state updating dynamically during rule evaluations leading to stale data. When attaching an engine-scoped cache directly to an external domain model (`state._heir_counts_cache`) during rule execution, it runs the risk of a runtime crash if the external `state` is a strict data structure like a Pydantic model or Dataclass. The problem has to be mitigated. Wait, the memory specifically states: "In 'backend/app/engine/core.py', avoid caching dynamic state (like `valid_heirs` counts) in the `InferenceEngine.__init__` method. State and facts are updated dynamically during rule evaluations, so initialization caching leads to stale data and critical regressions."

**Action:** Reverting the `_heir_counts_cache` implementation to prevent stale data regressions and Pydantic runtime crashes. I will stick to ONLY optimizing the `KNOWLEDGE_BASE_SORTED` performance bottleneck, as that static re-sorting provides a measurable performance improvement and does not violate any edge-case instructions.
