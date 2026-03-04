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
    # Case 8: Grandchildren only (substitution)
    run_test_case("Case 8: Son_of_Son + Daughter_of_Son", [
        Heir(relation="Son of Son", relation_type="Son_of_Son", lineage="paternal_descendant", gender="M", count=1, generation_level=2),
        Heir(relation="Daughter of Son", relation_type="Daughter_of_Son", lineage="paternal_descendant", gender="F", count=1, generation_level=2)
    ])

    # Case 12: Daughter blocks grandchildren
    run_test_case("Case 12: Daughter + Son_of_Son + Daughter_of_Son", [
        Heir(relation="Daughter", relation_type="Daughter", lineage="direct", gender="F", count=1, generation_level=1),
        Heir(relation="Son of Son", relation_type="Son_of_Son", lineage="paternal_descendant", gender="M", count=1, generation_level=2),
        Heir(relation="Daughter of Son", relation_type="Daughter_of_Son", lineage="paternal_descendant", gender="F", count=1, generation_level=2)
    ])

    # Case 13: Father + Grandson
    run_test_case("Case 13: Father + Son_of_Son", [
        Heir(relation="Father", relation_type="Father", lineage="direct", gender="M", count=1, generation_level=1),
        Heir(relation="Son of Son", relation_type="Son_of_Son", lineage="paternal_descendant", gender="M", count=1, generation_level=2)
    ])

    # Case 14: Depth Blocking
    run_test_case("Case 14: Son_of_Son + Son_of_Son_of_Son", [
        Heir(relation="Son of Son", relation_type="Son_of_Son", lineage="paternal_descendant", gender="M", count=1, generation_level=2),
        Heir(relation="Great Grandson", relation_type="Son_of_Son_of_Son", lineage="paternal_descendant", gender="M", count=1, generation_level=3)
    ])

    # Case 15: Mixed lines (Son line vs Daughter line)
    run_test_case("Case 15: Son_of_Son + Son_of_Daughter", [
        Heir(relation="Son of Son", relation_type="Son_of_Son", lineage="paternal_descendant", gender="M", count=1, generation_level=2),
        Heir(relation="Son of Daughter", relation_type="Son_of_Daughter", lineage="maternal_descendant", gender="M", count=1, generation_level=2)
    ])

    # Case 16: Daughters line vs Sons line (Specific example 1335)
    run_test_case("Case 16: Daughter_of_Son + Son_of_Daughter", [
        Heir(relation="Daughter of Son", relation_type="Daughter_of_Son", lineage="paternal_descendant", gender="F", count=1, generation_level=2),
        Heir(relation="Son of Daughter", relation_type="Son_of_Daughter", lineage="maternal_descendant", gender="M", count=1, generation_level=2)
    ])
