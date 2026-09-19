## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
## 2024-05-10 - O(1) Map lookups in list rendering
**Learning:** Re-filtering array items inside category iteration in React components (`categories.map(cat => list.filter(r => r.category === cat))`) combined with `list.find(...)` creates O(n^2) time complexity on every render pass.
**Action:** Replaced dynamic filtering with pre-computed `Map<string, Item[]>` for grouped items and `Map<string, SelectedItem>` for selected heir lookups, reducing render complexity to O(1) per card.

## 2024-05-14 - Python generator overhead and dynamic collections in hot loops
**Learning:** In Python, defining inner functions or dynamically instantiating collections (like `["Son", "Daughter", ...]`) within frequently called methods (hot loops, such as `evaluate_rule`, `_get_fact_value`, `fire_rule`, `resolve`) incurs continuous reallocation overhead and GC pressure. Using generator expressions (`all(...)`) inside these loops also creates significant generator overhead for small collections compared to native `for` loops with early returns.
**Action:** Extracted dynamic list instantiations to module-level static frozensets (`DESC_TYPES`, `C3_TYPES`, etc.) for O(1) lookups. Extracted inner closure functions into instance and static methods. Refactored `evaluate_rule` to use standard `for` loops with early returns instead of generators.

## 2024-05-18 - Pydantic deepcopy overhead with mutable defaults
**Learning:** In Pydantic v2 models, using mutable default arguments (like `[]`, `{}`, or `set()`) causes significant performance overhead because Pydantic implicitly runs a `copy.deepcopy()` during every single model instantiation. This overhead can be severe in hot paths (like repeatedly instantiating states during rule evaluation).
**Action:** Always use `Field(default_factory=list)`, `Field(default_factory=dict)`, or `Field(default_factory=set)` instead of mutable defaults in Pydantic models. Refactored `CaseState`, `CalculationStep`, and `CalculationResponse` to use `default_factory`, achieving a ~10x speedup in model instantiation.
