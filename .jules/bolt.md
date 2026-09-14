## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
## 2024-05-10 - O(1) Map lookups in list rendering
**Learning:** Re-filtering array items inside category iteration in React components (`categories.map(cat => list.filter(r => r.category === cat))`) combined with `list.find(...)` creates O(n^2) time complexity on every render pass.
**Action:** Replaced dynamic filtering with pre-computed `Map<string, Item[]>` for grouped items and `Map<string, SelectedItem>` for selected heir lookups, reducing render complexity to O(1) per card.

## 2024-05-14 - Python generator overhead and dynamic collections in hot loops
**Learning:** In Python, defining inner functions or dynamically instantiating collections (like `["Son", "Daughter", ...]`) within frequently called methods (hot loops, such as `evaluate_rule`, `_get_fact_value`, `fire_rule`, `resolve`) incurs continuous reallocation overhead and GC pressure. Using generator expressions (`all(...)`) inside these loops also creates significant generator overhead for small collections compared to native `for` loops with early returns.
**Action:** Extracted dynamic list instantiations to module-level static frozensets (`DESC_TYPES`, `C3_TYPES`, etc.) for O(1) lookups. Extracted inner closure functions into instance and static methods. Refactored `evaluate_rule` to use standard `for` loops with early returns instead of generators.


## 2024-05-18 - Pydantic mutable defaults overhead
**Learning:** In Pydantic models, using mutable default arguments (like `[]`, `{}`, or `set()`) causes significant performance overhead because Pydantic implicitly runs a `copy.deepcopy()` during every single model instantiation. This is particularly slow for classes that are instantiated frequently, like `CaseState`.
**Action:** Replaced mutable default arguments (e.g. `valid_heirs: List[Heir] = []`) with `Field(default_factory=...)` (e.g. `valid_heirs: List[Heir] = Field(default_factory=list)`) in `backend/app/engine/models.py`. This simple change yielded a measurable speedup (a drop in revalidation test times from ~0.66s to ~0.62s natively, and ~10x speedup in isolated microbenchmarks).
