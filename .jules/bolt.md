## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
## 2024-05-10 - O(1) Map lookups in list rendering
**Learning:** Re-filtering array items inside category iteration in React components (`categories.map(cat => list.filter(r => r.category === cat))`) combined with `list.find(...)` creates O(n^2) time complexity on every render pass.
**Action:** Replaced dynamic filtering with pre-computed `Map<string, Item[]>` for grouped items and `Map<string, SelectedItem>` for selected heir lookups, reducing render complexity to O(1) per card.

## 2024-05-14 - Python generator overhead and dynamic collections in hot loops
**Learning:** In Python, defining inner functions or dynamically instantiating collections (like `["Son", "Daughter", ...]`) within frequently called methods (hot loops, such as `evaluate_rule`, `_get_fact_value`, `fire_rule`, `resolve`) incurs continuous reallocation overhead and GC pressure. Using generator expressions (`all(...)`) inside these loops also creates significant generator overhead for small collections compared to native `for` loops with early returns.
**Action:** Extracted dynamic list instantiations to module-level static frozensets (`DESC_TYPES`, `C3_TYPES`, etc.) for O(1) lookups. Extracted inner closure functions into instance and static methods. Refactored `evaluate_rule` to use standard `for` loops with early returns instead of generators.

## 2026-09-17 - Pydantic v2 Mutable Defaults Overhead
**Learning:** In Pydantic v2, defining fields with mutable defaults (e.g., `[]`, `{}`) forces the framework to run an expensive `copy.deepcopy()` internally on every model instantiation to prevent shared-state side effects. Profiling the inference engine's `CaseState` allocation revealed this single issue was dominating initialization time.
**Action:** Replaced all empty lists, dicts, and sets in Pydantic models with `Field(default_factory=list)`, `Field(default_factory=dict)`, etc.

## 2026-09-17 - O(N) Array Scanning in Hot Generation Loops
**Learning:** Creating list comprehensions that linearly scan large static lists (like `KNOWLEDGE_BASE`) for matching string IDs inside hot resolution loops (e.g., retrieving `arabic_text` per rule, per heir) introduces hidden O(N) complexity per iteration.
**Action:** Replaced the linear scan `[rule.arabic_text for rule in KNOWLEDGE_BASE if rule.id == rid]` with an O(1) hash map lookup against the pre-existing, module-level `RULE_MAP` (`[RULE_MAP[rid].arabic_text for rid in rules]`), reducing execution time.
