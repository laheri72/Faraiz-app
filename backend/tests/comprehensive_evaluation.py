import sys
import os
from fractions import Fraction
# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.app.engine.core import EnginePipeline
from backend.app.engine.models import Heir

def test_runner():
    pipeline = EnginePipeline()
    
    # Define the 25 cases with engine-compatible mappings
    cases = [
        # T1: Grandson + Father
        {"id": "T1", "heirs": [
            Heir(relation="Father", relation_type="Father", lineage="direct", gender="M", count=1, generation_level=1),
            Heir(relation="Grandson", relation_type="Son_of_Son", lineage="paternal_descendant", gender="M", count=1, generation_level=2)
        ], "expected": {"father": "1/6", "grandson": "5/6"}},

        # T2: Granddaughter + Father
        {"id": "T2", "heirs": [
            Heir(relation="Father", relation_type="Father", lineage="direct", gender="M", count=1, generation_level=1),
            Heir(relation="Granddaughter", relation_type="Daughter_of_Son", lineage="paternal_descendant", gender="F", count=1, generation_level=2)
        ], "expected": {"father": "1/6", "granddaughter": "5/6"}},

        # T3: Daughter's Son + Father
        {"id": "T3", "heirs": [
            Heir(relation="Father", relation_type="Father", lineage="direct", gender="M", count=1, generation_level=1),
            Heir(relation="DaughtersSon", relation_type="Son_of_Daughter", lineage="maternal_descendant", gender="M", count=1, generation_level=2)
        ], "expected": {"father": "1/6", "daughtersson": "5/6"}},

        # T4: Wife + Parents + Grandmother + Son
        {"id": "T4", "heirs": [
            Heir(relation="Wife", relation_type="Wife", lineage="direct", gender="F", count=1, generation_level=1),
            Heir(relation="Father", relation_type="Father", lineage="direct", gender="M", count=1, generation_level=1),
            Heir(relation="Mother", relation_type="Mother", lineage="direct", gender="F", count=1, generation_level=1),
            Heir(relation="Grandmother", relation_type="grandmother_paternal", lineage="paternal", gender="F", count=1, generation_level=2),
            Heir(relation="Son", relation_type="Son", lineage="direct", gender="M", count=1, generation_level=1)
        ], "expected": {"wife": "1/8"}},

        # T5: Husband + Grandson + Granddaughter
        {"id": "T5", "heirs": [
            Heir(relation="Husband", relation_type="Husband", lineage="direct", gender="M", count=1, generation_level=1),
            Heir(relation="Grandson", relation_type="Son_of_Son", lineage="paternal_descendant", gender="M", count=1, generation_level=2),
            Heir(relation="Granddaughter", relation_type="Daughter_of_Son", lineage="paternal_descendant", gender="F", count=1, generation_level=2)
        ], "expected": {"husband": "1/4"}},

        # T6: Husband + Parents
        {"id": "T6", "heirs": [
            Heir(relation="Husband", relation_type="Husband", lineage="direct", gender="M", count=1, generation_level=1),
            Heir(relation="Father", relation_type="Father", lineage="direct", gender="M", count=1, generation_level=1),
            Heir(relation="Mother", relation_type="Mother", lineage="direct", gender="F", count=1, generation_level=1)
        ], "expected": {"husband": "1/2", "mother": "1/3", "father": "1/6"}},

        # T7: 2 Maternal Siblings
        {"id": "T7", "heirs": [
            Heir(relation="Mat Bro", relation_type="Brother_Maternal", lineage="maternal", gender="M", count=2, generation_level=1)
        ], "expected": {"maternal": "1"}},

        # T8: 1 Maternal Sibling
        {"id": "T8", "heirs": [
            Heir(relation="Mat Bro", relation_type="Brother_Maternal", lineage="maternal", gender="M", count=1, generation_level=1)
        ], "expected": {"maternal": "1"}},

        # T9: Maternal Nephews + Full Nephews
        {"id": "T9", "heirs": [
            Heir(relation="Full Nephew", relation_type="Son_of_Brother", lineage="paternal", gender="M", count=3, generation_level=2),
            Heir(relation="Mat Nephew", relation_type="Son_of_Sister", lineage="maternal", gender="M", count=2, generation_level=2)
        ], "expected": {"mat": "1/3", "full": "2/3"}},

        # T10: Grandfather + Nephew
        {"id": "T10", "heirs": [
            Heir(relation="Grandfather", relation_type="grandfather_paternal", lineage="paternal", gender="M", count=1, generation_level=2),
            Heir(relation="Nephew", relation_type="Son_of_Brother", lineage="paternal", gender="M", count=1, generation_level=2)
        ], "expected": {"grandfather": "1/2", "nephew": "1/2"}},

        # T11: Grandfather + 2 Maternal Siblings
        {"id": "T11", "heirs": [
            Heir(relation="Grandfather", relation_type="grandfather_paternal", lineage="paternal", gender="M", count=1, generation_level=2),
            Heir(relation="Mat Bro", relation_type="Brother_Maternal", lineage="maternal", gender="M", count=2, generation_level=1)
        ], "expected": {"maternal": "1/3", "grandfather": "2/3"}},

        # T12: Grandfather + 1 Maternal Sibling
        {"id": "T12", "heirs": [
            Heir(relation="Grandfather", relation_type="grandfather_paternal", lineage="paternal", gender="M", count=1, generation_level=2),
            Heir(relation="Mat Bro", relation_type="Brother_Maternal", lineage="maternal", gender="M", count=1, generation_level=1)
        ], "expected": {"maternal": "1/6", "grandfather": "5/6"}},

        # T13: Maternal Grandfather + Paternal Siblings
        {"id": "T13", "heirs": [
            Heir(relation="Maternal GF", relation_type="grandfather_maternal", lineage="maternal", gender="M", count=1, generation_level=2),
            Heir(relation="Brother", relation_type="Brother", lineage="paternal", gender="M", count=2, generation_level=1)
        ], "expected": {"maternal": "1/6", "brother": "5/6"}},

        # T14: 2 Grandmothers + Nephew
        {"id": "T14", "heirs": [
            Heir(relation="PGM", relation_type="grandmother_paternal", lineage="paternal", gender="F", count=1, generation_level=2),
            Heir(relation="MGM", relation_type="grandmother_maternal", lineage="maternal", gender="F", count=1, generation_level=2),
            Heir(relation="Nephew", relation_type="Son_of_Brother", lineage="paternal", gender="M", count=1, generation_level=2)
        ], "expected": {"grandmother": "1/3", "nephew": "2/3"}},

        # T15: Maternal GM + Paternal GM + Daughter
        {"id": "T15", "heirs": [
            Heir(relation="PGM", relation_type="grandmother_paternal", lineage="paternal", gender="F", count=1, generation_level=2),
            Heir(relation="MGM", relation_type="grandmother_maternal", lineage="maternal", gender="F", count=1, generation_level=2),
            Heir(relation="Daughter", relation_type="Daughter", lineage="direct", gender="F", count=1, generation_level=1)
        ], "expected": {"daughter": "2/3"}},

        # T16: Grandmother + Parents + 2 Siblings
        {"id": "T16", "heirs": [
            Heir(relation="Grandmother", relation_type="grandmother_paternal", lineage="paternal", gender="F", count=1, generation_level=2),
            Heir(relation="Father", relation_type="Father", lineage="direct", gender="M", count=1, generation_level=1),
            Heir(relation="Mother", relation_type="Mother", lineage="direct", gender="F", count=1, generation_level=1),
            Heir(relation="Brother", relation_type="Brother", lineage="paternal", gender="M", count=2, generation_level=1)
        ], "expected": {"grandmother": "1/6", "mother": "1/6", "father": "2/3"}},

        # T17: GM + GF + Full Brother + Paternal Brother
        {"id": "T17", "heirs": [
            Heir(relation="GM", relation_type="grandmother_paternal", lineage="paternal", gender="F", count=1, generation_level=2),
            Heir(relation="GF", relation_type="grandfather_paternal", lineage="paternal", gender="M", count=1, generation_level=2),
            Heir(relation="Full Bro", relation_type="Brother", lineage="paternal", gender="M", count=1, generation_level=1),
            Heir(relation="Pat Bro", relation_type="Brother", lineage="paternal", gender="M", count=1, generation_level=1)
        ], "expected": {"grandmother": "1/6"}},

        # T18: GM + Brother
        {"id": "T18", "heirs": [
            Heir(relation="GM", relation_type="grandmother_paternal", lineage="paternal", gender="F", count=1, generation_level=2),
            Heir(relation="Brother", relation_type="Brother", lineage="paternal", gender="M", count=1, generation_level=1)
        ], "expected": {"grandmother": "1/6"}},

        # T19: Full Aunt + Maternal Aunt
        {"id": "T19", "heirs": [
            Heir(relation="Full Aunt", relation_type="Paternal_Aunt", lineage="paternal", gender="F", count=1, generation_level=2),
            Heir(relation="Mat Aunt", relation_type="Maternal_Aunt", lineage="maternal", gender="F", count=1, generation_level=2)
        ], "expected": {"paternal": "2/3", "maternal": "1/3"}}, # Using engine defaults first

        # T20: Mat Uncle + Mat Aunt + Pat Uncle + Pat Aunt
        {"id": "T20", "heirs": [
            Heir(relation="Maternal Uncle", relation_type="Maternal_Uncle", lineage="maternal", gender="M", count=1, generation_level=2),
            Heir(relation="Maternal Aunt", relation_type="Maternal_Aunt", lineage="maternal", gender="F", count=1, generation_level=2),
            Heir(relation="Paternal Uncle", relation_type="Paternal_Uncle", lineage="paternal", gender="M", count=1, generation_level=2),
            Heir(relation="Paternal Aunt", relation_type="Paternal_Aunt", lineage="paternal", gender="F", count=1, generation_level=2)
        ], "expected": {"maternal": "1/3", "paternal": "2/3"}},

        # T21: Mat GF + Mat Uncle + Mat Aunt
        {"id": "T21", "heirs": [
            Heir(relation="Maternal GF", relation_type="grandfather_maternal", lineage="maternal", gender="M", count=1, generation_level=2),
            Heir(relation="Maternal Uncle", relation_type="Maternal_Uncle", lineage="maternal", gender="M", count=1, generation_level=2),
            Heir(relation="Maternal Aunt", relation_type="Maternal_Aunt", lineage="maternal", gender="F", count=1, generation_level=2)
        ], "expected": {"maternal": "1"}},

        # T22: Mat Uncle + Mat Aunt
        {"id": "T22", "heirs": [
            Heir(relation="Maternal Uncle", relation_type="Maternal_Uncle", lineage="maternal", gender="M", count=1, generation_level=2),
            Heir(relation="Maternal Aunt", relation_type="Maternal_Aunt", lineage="maternal", gender="F", count=1, generation_level=2)
        ], "expected": {"maternal": "1"}},

        # T23: Pat Aunt + Mat Aunt
        {"id": "T23", "heirs": [
            Heir(relation="Paternal Aunt", relation_type="Paternal_Aunt", lineage="paternal", gender="F", count=1, generation_level=2),
            Heir(relation="Maternal Aunt", relation_type="Maternal_Aunt", lineage="maternal", gender="F", count=1, generation_level=2)
        ], "expected": {"paternal": "2/3", "maternal": "1/3"}},

        # T24: Pat Uncle + Brother's Granddaughter
        {"id": "T24", "heirs": [
            Heir(relation="Paternal Uncle", relation_type="Paternal_Uncle", lineage="paternal", gender="M", count=1, generation_level=2),
            Heir(relation="BrothersGD", relation_type="Daughter_of_Son_of_Brother", lineage="paternal", gender="F", count=1, generation_level=3)
        ], "expected": {"brothersgd": "1"}},

        # T25: Mat Uncle + Sister's Son
        {"id": "T25", "heirs": [
            Heir(relation="Maternal Uncle", relation_type="Maternal_Uncle", lineage="maternal", gender="M", count=1, generation_level=2),
            Heir(relation="SistersSon", relation_type="Son_of_Sister", lineage="maternal", gender="M", count=1, generation_level=2)
        ], "expected": {"sistersson": "1"}}
    ]

    print(f"Running {len(cases)} check cases...\n")
    for c in cases:
        try:
            res = pipeline.calculate(c["heirs"], 120000)
            actual_shares = {}
            for r in res["results"]:
                if not r.is_blocked:
                    name_key = r.relation.lower().replace(" ", "").replace("_", "")
                    if "gm" in name_key or "grandmother" in name_key: name_key = "grandmother"
                    if "gf" in name_key or "grandfather" in name_key: name_key = "grandfather"
                    if "matnephew" in name_key: name_key = "matnephew"
                    if "fullnephew" in name_key: name_key = "fullnephew"
                    actual_shares[name_key] = actual_shares.get(name_key, Fraction(0)) + Fraction(r.share)
            
            mat_total = sum(Fraction(r.share) for r in res['results'] if not r.is_blocked and ("Maternal" in r.relation or "Mat" in r.relation))
            pat_total = sum(Fraction(r.share) for r in res['results'] if not r.is_blocked and ("Paternal" in r.relation or "Pat" in r.relation or "Uncle" in r.relation or "Aunt" in r.relation) and "Maternal" not in r.relation and "Mat" not in r.relation)
            full_total = sum(Fraction(r.share) for r in res['results'] if not r.is_blocked and ("Full" in r.relation))

            status = "FAIL"
            passed_checks = []
            for key, exp in c["expected"].items():
                k_low = key.lower()
                if k_low == "parents":
                    actual = actual_shares.get("father", 0) + actual_shares.get("mother", 0)
                elif k_low == "maternal":
                    actual = mat_total
                elif k_low == "paternal":
                    actual = pat_total
                elif k_low == "full":
                    actual = full_total
                elif k_low == "mat":
                    actual = sum(Fraction(r.share) for r in res['results'] if not r.is_blocked and "Mat" in r.relation)
                else:
                    actual = actual_shares.get(k_low, 0)
                
                if isinstance(exp, str) and "/" in exp:
                    if actual != Fraction(exp): passed_checks.append(False)
                    else: passed_checks.append(True)
                elif exp == "remainder":
                    passed_checks.append(True)
                else:
                    if actual != Fraction(exp): passed_checks.append(False)
                    else: passed_checks.append(True)
            
            if all(passed_checks): status = "PASS"
            print(f"[{status}] Case {c['id']}")
            if status == "FAIL":
                print(f"  Actual: {actual_shares} (Mat:{mat_total}, Pat:{pat_total}, Full:{full_total})")
                print(f"  Expected: {c['expected']}")
        except Exception as e:
            print(f"[ERROR] Case {c['id']}: {e}")

if __name__ == "__main__":
    test_runner()
