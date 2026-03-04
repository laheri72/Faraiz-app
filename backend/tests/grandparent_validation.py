import sys
import os
from fractions import Fraction
# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.app.engine.core import EnginePipeline
from backend.app.engine.models import Heir

def run_test_case(name, heirs, estate=100000):
    print(f"\n--- TEST CASE: {name} ---")
    pipeline = EnginePipeline()
    try:
        result = pipeline.calculate(heirs, estate)
        print(f"Status: {result['verification'].status}")
        print(f"Fraction Sum: {result['verification'].fraction_sum}")
        for r in result['results']:
            if not r.is_blocked:
                print(f"  {r.relation}: {r.share} (Amount: {r.amount})")
            else:
                print(f"  {r.relation}: BLOCKED by {r.blocked_by} ({r.blocking_rule_id})")
    except Exception as e:
        print(f"Error running test {name}: {e}")

if __name__ == "__main__":
    # Case 1 — Only PGF + PGM
    run_test_case("Case 1: PGF + PGM", [
        Heir(relation="PGF", relation_type="grandfather_paternal", lineage="paternal", gender="M", count=1, generation_level=2),
        Heir(relation="PGM", relation_type="grandmother_paternal", lineage="paternal", gender="F", count=1, generation_level=2)
    ])

    # Case 2 — Only MGF + MGM
    run_test_case("Case 2: MGF + MGM", [
        Heir(relation="MGF", relation_type="grandfather_maternal", lineage="maternal", gender="M", count=1, generation_level=2),
        Heir(relation="MGM", relation_type="grandmother_maternal", lineage="maternal", gender="F", count=1, generation_level=2)
    ])

    # Case 19 — PGF + 2 Maternal Siblings
    run_test_case("Case 19: PGF + 2 Maternal Siblings", [
        Heir(relation="PGF", relation_type="grandfather_paternal", lineage="paternal", gender="M", count=1, generation_level=2),
        Heir(relation="Maternal Brother", relation_type="Brother_Maternal", lineage="maternal", gender="M", count=2, generation_level=1)
    ])

    # Case 3 — All Four Grandparents
    run_test_case("Case 3: All Four Grandparents", [
        Heir(relation="PGF", relation_type="grandfather_paternal", lineage="paternal", gender="M", count=1, generation_level=2),
        Heir(relation="PGM", relation_type="grandmother_paternal", lineage="paternal", gender="F", count=1, generation_level=2),
        Heir(relation="MGF", relation_type="grandfather_maternal", lineage="maternal", gender="M", count=1, generation_level=2),
        Heir(relation="MGM", relation_type="grandmother_maternal", lineage="maternal", gender="F", count=1, generation_level=2)
    ])
