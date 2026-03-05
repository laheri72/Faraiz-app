import sys
import os
from fractions import Fraction
# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.app.engine.core import EnginePipeline
from backend.app.engine.models import Heir

def run_arham_case(case_id, heirs, expected, estate=120000):
    pipeline = EnginePipeline()
    try:
        result = pipeline.calculate(heirs, estate)
        actual = {}
        for r in result['results']:
            if not r.is_blocked:
                # Use relation name or heir_id mappings to match expected keys
                key = r.relation.replace(" ", "_")
                if key == "Paternal_Aunt": key = "Aunt_paternal"
                elif key == "Maternal_Aunt": key = "Aunt_maternal"
                elif key == "Paternal_Uncle": key = "Uncle_paternal"
                elif key == "Maternal_Uncle": key = "Uncle_maternal"
                elif key == "Son_of_Pat_Aunt": key = "Son_of_aunt"
                elif key == "Daughter_of_Pat_Uncle": key = "Daughter_of_uncle"
                elif key == "Maternal_Cousin": key = "Son_of_maternal_uncle"
                
                val = Fraction(r.share)
                actual[key] = actual.get(key, Fraction(0)) + val
        
        # side totals
        mat_total = sum(Fraction(r.share) for r in result['results'] if not r.is_blocked and ("Maternal" in r.relation or "Mat" in r.relation))
        pat_total = sum(Fraction(r.share) for r in result['results'] if not r.is_blocked and ("Paternal" in r.relation or "Pat" in r.relation or "Uncle" in r.relation or "Aunt" in r.relation) and "Maternal" not in r.relation and "Mat" not in r.relation)
        
        actual["Maternal_side_total"] = mat_total
        actual["Paternal_side_total"] = pat_total

        passed = True
        for key, exp_str in expected.items():
            if key not in actual and key != "Rule":
                passed = False
                break
            if key == "Rule": continue
            if actual[key] != Fraction(exp_str):
                passed = False
                break
        
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {case_id}")
        if not passed:
            print(f"  Actual: {actual}")
            print(f"  Expected: {expected}")
        return passed
    except Exception as e:
        print(f"[ERROR] {case_id}: {e}")
        return False

if __name__ == "__main__":
    print("\n=== RUNNING DHAWU AL-ARHAM SUITE VALIDATION ===\n")
    
    # A1: Aunt_paternal + Aunt_maternal
    run_arham_case("A1", [
        Heir(relation="Paternal Aunt", relation_type="Paternal_Aunt", lineage="paternal", gender="F", count=1, generation_level=2),
        Heir(relation="Maternal Aunt", relation_type="Maternal_Aunt", lineage="maternal", gender="F", count=1, generation_level=2)
    ], {"Aunt_paternal": "2/3", "Aunt_maternal": "1/3"})

    # A2: All 4
    run_arham_case("A2", [
        Heir(relation="Paternal Uncle", relation_type="Paternal_Uncle", lineage="paternal", gender="M", count=1, generation_level=2),
        Heir(relation="Paternal Aunt", relation_type="Paternal_Aunt", lineage="paternal", gender="F", count=1, generation_level=2),
        Heir(relation="Maternal Uncle", relation_type="Maternal_Uncle", lineage="maternal", gender="M", count=1, generation_level=2),
        Heir(relation="Maternal Aunt", relation_type="Maternal_Aunt", lineage="maternal", gender="F", count=1, generation_level=2)
    ], {"Maternal_side_total": "1/3", "Paternal_side_total": "2/3"})

    # A3: Mat Cousin vs Pat Uncle/Aunt
    run_arham_case("A3", [
        Heir(relation="Maternal Cousin", relation_type="Son_of_Maternal_Uncle", lineage="maternal", gender="M", count=1, generation_level=3),
        Heir(relation="Paternal Uncle", relation_type="Paternal_Uncle", lineage="paternal", gender="M", count=1, generation_level=2),
        Heir(relation="Paternal Aunt", relation_type="Paternal_Aunt", lineage="paternal", gender="F", count=1, generation_level=2)
    ], {"Uncle_paternal": "2/3", "Aunt_paternal": "1/3"})

    # A4: Pat Cousins vs Mat Uncles
    run_arham_case("A4", [
        Heir(relation="Paternal Cousin", relation_type="Son_of_Paternal_Uncle", lineage="paternal", gender="M", count=2, generation_level=3),
        Heir(relation="Maternal Uncle", relation_type="Maternal_Uncle", lineage="maternal", gender="M", count=1, generation_level=2),
        Heir(relation="Maternal Aunt", relation_type="Maternal_Aunt", lineage="maternal", gender="F", count=1, generation_level=2)
    ], {"Maternal_side_total": "1"})

    # A5: Son of Aunt vs Daughter of Uncle (Paternal)
    run_arham_case("A5", [
        Heir(relation="Son of Pat Aunt", relation_type="Son_of_Paternal_Aunt", lineage="paternal", gender="M", count=1, generation_level=3),
        Heir(relation="Daughter of Pat Uncle", relation_type="Daughter_of_Paternal_Uncle", lineage="paternal", gender="F", count=1, generation_level=3)
    ], {"Son_of_aunt": "2/3", "Daughter_of_uncle": "1/3"})

    # A7: Closest blocks further
    run_arham_case("A7", [
        Heir(relation="Son", relation_type="Son", lineage="direct", gender="M", count=1, generation_level=1),
        Heir(relation="Grandson", relation_type="Son_of_Son", lineage="paternal_descendant", gender="M", count=1, generation_level=2)
    ], {"Son": "1"})

    # A8: Daughter overrides Uncle
    run_arham_case("A8", [
        Heir(relation="Daughter", relation_type="Daughter", lineage="direct", gender="F", count=1, generation_level=1),
        Heir(relation="Paternal Uncle", relation_type="Paternal_Uncle", lineage="paternal", gender="M", count=1, generation_level=2)
    ], {"Daughter": "1"})
