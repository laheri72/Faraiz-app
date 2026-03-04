import sys
import os
from fractions import Fraction
# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.app.engine.core import EnginePipeline
from backend.app.engine.models import Heir

def run_test_case(name, heirs, estate=20000):
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
    # The failing case: 1 Wife, 1 Brother, 1 Son of Brother
    run_test_case("Wife + Brother + Nephew", [
        Heir(relation="Wife", relation_type="Wife", lineage="direct", gender="F", count=1, generation_level=1),
        Heir(relation="Brother", relation_type="Brother", lineage="paternal", gender="M", count=1, generation_level=1),
        Heir(relation="Nephew", relation_type="Son_of_Brother", lineage="paternal", gender="M", count=1, generation_level=2)
    ])
