import sys
import os
from fractions import Fraction
# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.app.engine.core import EnginePipeline
from backend.app.engine.models import Heir

def run_test_case(case_id, heirs, expected):
    pipeline = EnginePipeline()
    try:
        result = pipeline.calculate(heirs, 120000)
        actual = {}
        for r in result['results']:
            if not r.is_blocked:
                # Map actual relation_type to expected key
                key = r.relation
                # Check for pool matches in expected
                if "Full Brother" in expected and r.relation == "Full Brother": key = "Full Brother"
                elif "Brother" in expected and r.relation == "Brother": key = "Brother"
                elif "Full Bro" in expected and r.relation == "Full Bro": key = "Full Bro"
                elif "Sister" in expected and r.relation == "Sister": key = "Sister"
                elif "Mat Bro" in expected and r.relation == "Mat Bro": key = "Mat Bro"
                elif "Mat Sis" in expected and r.relation == "Mat Sis": key = "Mat Sis"
                elif "grandfather_paternal" in expected and r.relation.startswith("PGF"): key = "grandfather_paternal"
                elif "grandmother_paternal" in expected and r.relation.startswith("PGM"): key = "grandmother_paternal"
                elif "grandfather_maternal" in expected and r.relation.startswith("MGF"): key = "grandfather_maternal"
                elif "grandmother_maternal" in expected and r.relation.startswith("MGM"): key = "grandmother_maternal"

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
        print(f"[{status}] Case {case_id}: {actual} (Expected: {expected})")
        return passed
    except Exception as e:
        print(f"[ERROR] Case {case_id}: {e}")
        return False

if __name__ == "__main__":
    print("\n=== RUNNING 27 AUTHORITATIVE TEST CASES ===\n")
    
    cases = [
        ("T1", [Heir(relation="Father", relation_type="Father", lineage="direct", gender="M", count=1, generation_level=1), Heir(relation="Mother", relation_type="Mother", lineage="direct", gender="F", count=1, generation_level=1)], {"Father":"2/3","Mother":"1/3"}),
        ("T2", [Heir(relation="Father", relation_type="Father", lineage="direct", gender="M", count=1, generation_level=1), Heir(relation="Mother", relation_type="Mother", lineage="direct", gender="F", count=1, generation_level=1), Heir(relation="Son", relation_type="Son", lineage="direct", gender="M", count=1, generation_level=1)], {"Father":"1/6","Mother":"1/6","Son":"2/3"}),
        ("T3", [Heir(relation="Father", relation_type="Father", lineage="direct", gender="M", count=1, generation_level=1), Heir(relation="Mother", relation_type="Mother", lineage="direct", gender="F", count=1, generation_level=1), Heir(relation="Son", relation_type="Son", lineage="direct", gender="M", count=1, generation_level=1), Heir(relation="Daughter", relation_type="Daughter", lineage="direct", gender="F", count=1, generation_level=1)], {"Father":"1/6","Mother":"1/6","Son":"4/9","Daughter":"2/9"}),
        ("T4", [Heir(relation="Father", relation_type="Father", lineage="direct", gender="M", count=1, generation_level=1), Heir(relation="Mother", relation_type="Mother", lineage="direct", gender="F", count=1, generation_level=1), Heir(relation="Daughter", relation_type="Daughter", lineage="direct", gender="F", count=1, generation_level=1)], {"Father":"1/6","Mother":"1/6","Daughter":"2/3"}),
        ("T5", [Heir(relation="Mother", relation_type="Mother", lineage="direct", gender="F", count=1, generation_level=1), Heir(relation="Daughter", relation_type="Daughter", lineage="direct", gender="F", count=1, generation_level=1)], {"Mother":"1/6","Daughter":"5/6"}),
        ("T6", [Heir(relation="Father", relation_type="Father", lineage="direct", gender="M", count=1, generation_level=1), Heir(relation="Daughter", relation_type="Daughter", lineage="direct", gender="F", count=1, generation_level=1)], {"Father":"1/6","Daughter":"5/6"}),
        ("T7", [Heir(relation="Father", relation_type="Father", lineage="direct", gender="M", count=1, generation_level=1), Heir(relation="Mother", relation_type="Mother", lineage="direct", gender="F", count=1, generation_level=1), Heir(relation="Brother", relation_type="Brother", lineage="paternal", gender="M", count=2, generation_level=1)], {"Mother":"1/6","Father":"5/6"}),
        ("T8", [Heir(relation="Father", relation_type="Father", lineage="direct", gender="M", count=1, generation_level=1), Heir(relation="Mother", relation_type="Mother", lineage="direct", gender="F", count=1, generation_level=1), Heir(relation="Maternal Brother", relation_type="Brother_Maternal", lineage="maternal", gender="M", count=2, generation_level=1)], {"Mother":"1/3","Father":"2/3"}),
        ("T9", [Heir(relation="Mother", relation_type="Mother", lineage="direct", gender="F", count=1, generation_level=1), Heir(relation="Full Brother", relation_type="Brother", lineage="paternal", gender="M", count=2, generation_level=1)], {"Mother":"1"}),
        ("T10", [Heir(relation="Husband", relation_type="Husband", lineage="direct", gender="M", count=1, generation_level=1)], {"Husband":"1"}),
        ("T11", [Heir(relation="Wife", relation_type="Wife", lineage="direct", gender="F", count=1, generation_level=1)], {"Wife":"1"}),
        ("T12", [Heir(relation="Husband", relation_type="Husband", lineage="direct", gender="M", count=1, generation_level=1), Heir(relation="Son", relation_type="Son", lineage="direct", gender="M", count=1, generation_level=1)], {"Husband":"1/4","Son":"3/4"}),
        ("T13", [Heir(relation="Wife", relation_type="Wife", lineage="direct", gender="F", count=1, generation_level=1), Heir(relation="Son", relation_type="Son", lineage="direct", gender="M", count=1, generation_level=1)], {"Wife":"1/8","Son":"7/8"}),
        ("T14", [Heir(relation="Wife", relation_type="Wife", lineage="direct", gender="F", count=1, generation_level=1), Heir(relation="Father", relation_type="Father", lineage="direct", gender="M", count=1, generation_level=1), Heir(relation="Mother", relation_type="Mother", lineage="direct", gender="F", count=1, generation_level=1)], {"Wife":"1/4","Mother":"1/3","Father":"5/12"}),
        ("T15", [Heir(relation="Husband", relation_type="Husband", lineage="direct", gender="M", count=1, generation_level=1), Heir(relation="Father", relation_type="Father", lineage="direct", gender="M", count=1, generation_level=1), Heir(relation="Mother", relation_type="Mother", lineage="direct", gender="F", count=1, generation_level=1)], {"Husband":"1/2","Mother":"1/3","Father":"1/6"}),
        ("T16", [Heir(relation="Sister", relation_type="Sister", lineage="paternal", gender="F", count=1, generation_level=1)], {"Sister":"1"}),
        ("T17", [Heir(relation="Sister", relation_type="Sister", lineage="paternal", gender="F", count=2, generation_level=1)], {"Sister":"1"}),
        ("T18", [Heir(relation="Brother", relation_type="Brother", lineage="paternal", gender="M", count=1, generation_level=1), Heir(relation="Sister", relation_type="Sister", lineage="paternal", gender="F", count=1, generation_level=1)], {"Brother":"2/3","Sister":"1/3"}),
        ("T19", [Heir(relation="Mat Bro", relation_type="Brother_Maternal", lineage="maternal", gender="M", count=1, generation_level=1)], {"Mat Bro":"1"}),
        ("T20", [Heir(relation="Mat Bro", relation_type="Brother_Maternal", lineage="maternal", gender="M", count=2, generation_level=1)], {"Mat Bro":"1"}),
        ("T21", [Heir(relation="Full Bro", relation_type="Brother", lineage="paternal", gender="M", count=1, generation_level=1), Heir(relation="Mat Bro", relation_type="Brother_Maternal", lineage="maternal", gender="M", count=1, generation_level=1)], {"Full Bro":"2/3","Mat Bro":"1/3"}),
        ("T22", [Heir(relation="Full Bro", relation_type="Brother", lineage="paternal", gender="M", count=1, generation_level=1), Heir(relation="Mat Sis", relation_type="Sister_Maternal", lineage="maternal", gender="F", count=1, generation_level=1)], {"Full Bro":"2/3","Mat Sis":"1/3"}),
        ("T23", [Heir(relation="PGF", relation_type="grandfather_paternal", lineage="paternal", gender="M", count=1, generation_level=2), Heir(relation="Full Bro", relation_type="Brother", lineage="paternal", gender="M", count=1, generation_level=1)], {"grandfather_paternal":"1/2","Full Bro":"1/2"}),
        ("T24", [Heir(relation="PGF", relation_type="grandfather_paternal", lineage="paternal", gender="M", count=1, generation_level=2), Heir(relation="Nephew", relation_type="Son_of_Brother", lineage="paternal", gender="M", count=1, generation_level=2)], {"grandfather_paternal":"1/2","Nephew":"1/2"}),
        ("T25", [Heir(relation="PGF", relation_type="grandfather_paternal", lineage="paternal", gender="M", count=1, generation_level=2), Heir(relation="PGM", relation_type="grandmother_paternal", lineage="paternal", gender="F", count=1, generation_level=2)], {"grandfather_paternal":"2/3","grandmother_paternal":"1/3"}),
        ("T26", [Heir(relation="PGF", relation_type="grandfather_paternal", lineage="paternal", gender="M", count=1, generation_level=2), Heir(relation="PGM", relation_type="grandmother_paternal", lineage="paternal", gender="F", count=1, generation_level=2), Heir(relation="MGF", relation_type="grandfather_maternal", lineage="maternal", gender="M", count=1, generation_level=2), Heir(relation="MGM", relation_type="grandmother_maternal", lineage="maternal", gender="F", count=1, generation_level=2)], {"grandfather_paternal":"4/9", "grandmother_paternal":"2/9", "grandfather_maternal":"1/6", "grandmother_maternal":"1/6"}),
        ("T27", [Heir(relation="Grandmother", relation_type="grandmother_paternal", lineage="paternal", gender="F", count=1, generation_level=2)], {"Grandmother":"1"})
    ]

    total_passed = 0
    for c_id, heirs, expected in cases:
        if run_test_case(c_id, heirs, expected):
            total_passed += 1
    
    print(f"\nSummary: {total_passed}/{len(cases)} cases passed.")
