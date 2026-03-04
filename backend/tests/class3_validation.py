import sys
import os
from fractions import Fraction
# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.app.engine.core import EnginePipeline
from backend.app.engine.models import Heir

def run_test_case(case_id, heirs, expected, estate=120000):
    pipeline = EnginePipeline()
    try:
        result = pipeline.calculate(heirs, estate)
        actual = {}
        for r in result['results']:
            if not r.is_blocked:
                # Map actual relation to expected key
                key = r.relation
                if "PGF" in expected and r.relation == "grandfather_paternal": key = "PGF"
                
                val = Fraction(r.share)
                actual[key] = actual.get(key, Fraction(0)) + val

        passed = True
        for key, exp_str in expected.items():
            exp_val = Fraction(exp_str)
            act_val = actual.get(key, Fraction(0))
            if act_val != exp_val:
                passed = False
                break
        
        status = "PASS" if (passed and result['verification'].status == "VALID") else "FAIL"
        print(f"[{status}] {case_id}")
        if not passed:
            print(f"  Actual: {actual}")
            print(f"  Expected: {expected}")
        return passed
    except Exception as e:
        print(f"[ERROR] {case_id}: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n=== RUNNING CLASS 3 (UNCLES/AUNTS) VALIDATION ===\n")
    
    cases = [
        # Case 1: Paternal Aunt + Maternal Aunt (1356)
        # Paternal side gets 2/3, Maternal side gets 1/3
        ("Case 1: Pat Aunt + Mat Aunt", [
            Heir(relation="Paternal Aunt", relation_type="Paternal_Aunt", lineage="paternal", gender="F", count=1, generation_level=2),
            Heir(relation="Maternal Aunt", relation_type="Maternal_Aunt", lineage="maternal", gender="F", count=1, generation_level=2)
        ], {"Paternal Aunt": "2/3", "Maternal Aunt": "1/3"}),

        # Case 2: Uncle + Aunt + Maternal Uncle + Maternal Aunt (1357)
        # Maternal side 1/3 shared 1:1. Paternal side 2/3 shared 2:1.
        ("Case 2: All 4 Uncles/Aunts", [
            Heir(relation="Paternal Uncle", relation_type="Paternal_Uncle", lineage="paternal", gender="M", count=1, generation_level=2),
            Heir(relation="Paternal Aunt", relation_type="Paternal_Aunt", lineage="paternal", gender="F", count=1, generation_level=2),
            Heir(relation="Maternal Uncle", relation_type="Maternal_Uncle", lineage="maternal", gender="M", count=1, generation_level=2),
            Heir(relation="Maternal Aunt", relation_type="Maternal_Aunt", lineage="maternal", gender="F", count=1, generation_level=2)
        ], {
            "Paternal Uncle": "4/9", "Paternal Aunt": "2/9", 
            "Maternal Uncle": "1/6", "Maternal Aunt": "1/6"
        }),

        # Case 3: Uncle + Aunt + Maternal Cousin (1357)
        # Uncles block cousins.
        ("Case 3: Pat Uncle/Aunt vs Mat Cousin", [
            Heir(relation="Paternal Uncle", relation_type="Paternal_Uncle", lineage="paternal", gender="M", count=1, generation_level=2),
            Heir(relation="Paternal Aunt", relation_type="Paternal_Aunt", lineage="paternal", gender="F", count=1, generation_level=2),
            Heir(relation="Maternal Cousin", relation_type="Son_of_Maternal_Uncle", lineage="maternal", gender="M", count=1, generation_level=3)
        ], {"Paternal Uncle": "2/3", "Paternal Aunt": "1/3"}),

        # Case 4: Paternal Cousins + Maternal Uncle/Aunt (1357)
        # Closer blocks further. Maternal side takes everything because they are closer.
        ("Case 4: Pat Cousins vs Mat Uncle/Aunt", [
            Heir(relation="Paternal Cousin M", relation_type="Son_of_Paternal_Uncle", lineage="paternal", gender="M", count=1, generation_level=3),
            Heir(relation="Paternal Cousin F", relation_type="Daughter_of_Paternal_Uncle", lineage="paternal", gender="F", count=1, generation_level=3),
            Heir(relation="Maternal Aunt", relation_type="Maternal_Aunt", lineage="maternal", gender="F", count=1, generation_level=2)
        ], {"Maternal Aunt": "1"}),

        # Case 5: Substitution - Son of Aunt + Daughter of Uncle (1357)
        # They inherit parent's share.
        ("Case 5: Cousins substitution", [
            Heir(relation="Son of Pat Aunt", relation_type="Son_of_Paternal_Aunt", lineage="paternal", gender="M", count=1, generation_level=3),
            Heir(relation="Daughter of Pat Uncle", relation_type="Daughter_of_Paternal_Uncle", lineage="paternal", gender="F", count=1, generation_level=3)
        ], {
            "Son of Pat Aunt": "1/3", 
            "Daughter of Pat Uncle": "2/3"
        })
    ]

    total_passed = 0
    for c_id, heirs, expected in cases:
        if run_test_case(c_id, heirs, expected):
            total_passed += 1
    
    print(f"\nSummary: {total_passed}/{len(cases)} cases passed.")
