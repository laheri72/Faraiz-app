import sys
import os
from fractions import Fraction
# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.app.engine.core import EnginePipeline
from backend.app.engine.models import Heir

def run_test_case(name, heirs, estate=120000):
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
    # Case 1: Male + Female children only (2:1 ratio)
    run_test_case("Case 1: 1 Son + 1 Daughter", [
        Heir(relation="Son", relation_type="Son", lineage="direct", gender="M", count=1, generation_level=1),
        Heir(relation="Daughter", relation_type="Daughter", lineage="direct", gender="F", count=1, generation_level=1)
    ])

    # Case 2: Single son only
    run_test_case("Case 2: Single Son", [
        Heir(relation="Son", relation_type="Son", lineage="direct", gender="M", count=1, generation_level=1)
    ])

    # Case 3: Single daughter only (1/2 + 1/2 radd)
    run_test_case("Case 3: Single Daughter", [
        Heir(relation="Daughter", relation_type="Daughter", lineage="direct", gender="F", count=1, generation_level=1)
    ])

    # Case 4: Two daughters only (2/3 + 1/3 radd)
    run_test_case("Case 4: Two Daughters", [
        Heir(relation="Daughter", relation_type="Daughter", lineage="direct", gender="F", count=2, generation_level=1)
    ])

    # Case 7: Children + Other Fixed Share (Husband + Son)
    run_test_case("Case 7: Husband + Son", [
        Heir(relation="Husband", relation_type="Husband", lineage="direct", gender="M", count=1, generation_level=1),
        Heir(relation="Son", relation_type="Son", lineage="direct", gender="M", count=1, generation_level=1)
    ])

    # Complex: Wife + Mother + Father + 2 Daughters
    run_test_case("Complex: Wife + Mother + Father + 2 Daughters", [
        Heir(relation="Wife", relation_type="Wife", lineage="direct", gender="F", count=1, generation_level=1),
        Heir(relation="Mother", relation_type="Mother", lineage="direct", gender="F", count=1, generation_level=1),
        Heir(relation="Father", relation_type="Father", lineage="direct", gender="M", count=1, generation_level=1),
        Heir(relation="Daughter", relation_type="Daughter", lineage="direct", gender="F", count=2, generation_level=1)
    ])
