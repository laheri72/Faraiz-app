## 2024-05-06 - React referential equality edge case in lists
**Learning:** Using React.memo on a list item requires modifying its event handlers. If the parent passes inline closures (e.g., `onAdd={() => handleAdd(item)}`), `React.memo` will always fail shallow comparison because the function reference changes every render. The child MUST be refactored to accept generic stable handlers and its own identifiers.
**Action:** Changed `RelationCard` props to accept identifiers and stable `useCallback` functions.

## 2024-05-07 - Python Closure Allocation Overhead in Hot Loops
**Learning:** In highly repetitive fact-evaluation loops (like `_get_fact_value`), using inner functions defined within the loop (e.g., `def get_count(target): ...`) incurs continuous closure allocation overhead on every method invocation, significantly slowing down rule processing.
**Action:** Replace dynamically created inner functions and lists in hot loops with static module-level sets and inline dict lookups (e.g., `cnt.get(rel_type, 0)`) to achieve >50% speedup in constant time evaluation logic without changing functionality.
