import sys
import os
import json
from fractions import Fraction
from typing import List, Dict, Any

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.app.engine.core import EnginePipeline
from backend.app.engine.models import Heir

# Mapping from test case heir names to engine relation_types
HEIR_MAPPING = {
    "PGF": ("PGF", "grandfather_paternal", "paternal", "M", 2),
    "PGM": ("PGM", "grandmother_paternal", "paternal", "F", 2),
    "MGF": ("MGF", "grandfather_maternal", "maternal", "M", 2),
    "MGM": ("MGM", "grandmother_maternal", "maternal", "F", 2),
    "Father": ("Father", "Father", "direct", "M", 1),
    "Mother": ("Mother", "Mother", "direct", "F", 1),
    "Son": ("Son", "Son", "direct", "M", 1),
    "Daughter": ("Daughter", "Daughter", "direct", "F", 1),
    "Husband": ("Husband", "Husband", "direct", "M", 1),
    "Wife": ("Wife", "Wife", "direct", "F", 1),
    "Brother": ("Brother", "Brother", "paternal", "M", 1),
    "Sister": ("Sister", "Sister", "paternal", "F", 1),
    "Brother_full": ("Brother", "Brother", "paternal", "M", 1),
    "Sister_full": ("Sister", "Sister", "paternal", "F", 1),
    "Brother_maternal": ("Mat Bro", "Brother_Maternal", "maternal", "M", 1),
    "Sister_maternal": ("Mat Sis", "Sister_Maternal", "maternal", "F", 1),
    "Nephew": ("Nephew", "Son_of_Brother", "paternal", "M", 2),
    "Son_of_Son": ("Grandson", "Son_of_Son", "paternal_descendant", "M", 2),
    "Daughter_of_Son": ("Granddaughter", "Daughter_of_Son", "paternal_descendant", "F", 2),
    "Son_of_Daughter": ("Daughter's Son", "Son_of_Daughter", "maternal_descendant", "M", 2),
    "Daughter_of_Daughter": ("Daughter's Daughter", "Daughter_of_Daughter", "maternal_descendant", "F", 2),
    "Aunt_paternal": ("Paternal Aunt", "Paternal_Aunt", "paternal", "F", 3),
    "Aunt_maternal": ("Maternal Aunt", "Maternal_Aunt", "maternal", "F", 3),
    "Uncle_paternal": ("Paternal Uncle", "Paternal_Uncle", "paternal", "M", 3),
    "Uncle_maternal": ("Maternal Uncle", "Maternal_Uncle", "maternal", "M", 3),
    "Son_of_maternal_uncle": ("Maternal Cousin", "Son_of_Maternal_Uncle", "maternal", "M", 4),
    "Cousin_paternal": ("Paternal Cousin", "Son_of_Paternal_Uncle", "paternal", "M", 4),
    "Son_of_aunt": ("Aunt's Son", "Son_of_Paternal_Aunt", "paternal", "M", 4),
    "Daughter_of_uncle": ("Uncle's Daughter", "Daughter_of_Paternal_Uncle", "paternal", "F", 4),
    "Grandson": ("Grandson", "Son_of_Son", "paternal_descendant", "M", 2),
    "Granddaughter": ("Granddaughter", "Daughter_of_Son", "paternal_descendant", "F", 2),
    "DaughtersSon": ("Daughter's Son", "Son_of_Daughter", "maternal_descendant", "M", 2),
    "MaternalSibling": ("Mat Sibling", "Brother_Maternal", "maternal", "M", 1),
    "FullNephews": ("Full Nephew", "Son_of_Brother", "paternal", "M", 2),
    "MaternalNephews": ("Mat Nephew", "Son_of_Sister", "maternal", "M", 2),
    "Grandfather": ("Grandfather", "grandfather_paternal", "paternal", "M", 2),
    "Grandmother": ("Grandmother", "grandmother_paternal", "paternal", "F", 2),
    "MaternalSiblings": ("Mat Siblings", "Brother_Maternal", "maternal", "M", 1),
    "MaternalGrandfather": ("Maternal GF", "grandfather_maternal", "maternal", "M", 2),
    "PaternalSiblings": ("Brother", "Brother", "paternal", "M", 1),
    "Grandmothers": ("Grandmother", "grandmother_paternal", "paternal", "F", 2),
    "GrandmotherMaternal": ("MGM", "grandmother_maternal", "maternal", "F", 2),
    "GrandmotherPaternal": ("PGM", "grandmother_paternal", "paternal", "F", 2),
    "Siblings": ("Brother", "Brother", "paternal", "M", 1),
    "BrotherFull": ("Brother", "Brother", "paternal", "M", 1),
    "BrotherPaternal": ("Brother", "Brother", "paternal", "M", 1),
    "FullAunt": ("Paternal Aunt", "Paternal_Aunt", "paternal", "F", 3),
    "MaternalAunt": ("Maternal Aunt", "Maternal_Aunt", "maternal", "F", 3),
    "MaternalUncle": ("Maternal Uncle", "Maternal_Uncle", "maternal", "M", 3),
    "PaternalUncle": ("Paternal Uncle", "Paternal_Uncle", "paternal", "M", 3),
    "PaternalAunt": ("Paternal Aunt", "Paternal_Aunt", "paternal", "F", 3),
    "BrothersGranddaughter": ("BrothersGD", "Daughter_of_Son_of_Brother", "paternal", "F", 3),
    "SistersSon": ("SistersSon", "Son_of_Sister", "maternal", "M", 2),
    "Each_Son": ("Son", "Son", "direct", "M", 1),
    "Each_Sister": ("Sister", "Sister", "paternal", "F", 1),
    "Grandfather_paternal": ("PGF", "grandfather_paternal", "paternal", "M", 2),
    "Grandmother_paternal": ("PGM", "grandmother_paternal", "paternal", "F", 2),
    "Grandfather_maternal": ("MGF", "grandfather_maternal", "maternal", "M", 2),
    "Grandmother_maternal": ("MGM", "grandmother_maternal", "maternal", "F", 2),
    "Each_Daughter": ("Daughter", "Daughter", "direct", "F", 1),
}

def create_heir(name: str, count: int) -> Heir:
    if name in HEIR_MAPPING:
        rel, rel_type, lineage, gender, level = HEIR_MAPPING[name]
        return Heir(relation=rel, relation_type=rel_type, lineage=lineage, gender=gender, count=count, generation_level=level)
    return Heir(relation=name, relation_type=name, lineage="direct", gender="M", count=count, generation_level=1)

def run_test_suite(suite_name: str, cases: List[Dict[str, Any]]):
    pipeline = EnginePipeline()
    passed = 0
    failed = []
    for case in cases:
        case_id = case.get("id") or case.get("case_id")
        heirs_input = case.get("heirs", [])
        heirs_list = []
        if isinstance(heirs_input, dict):
            for name, count in heirs_input.items(): heirs_list.append(create_heir(name, count))
        elif isinstance(heirs_input, list):
            for h in heirs_input: heirs_list.append(create_heir(h["relation"], h.get("count", 1)))
        
        estate = float(case.get("estate", 120000))
        try:
            result = pipeline.calculate(heirs_list, estate)
            if result["verification"].status == "VALID": passed += 1
            else: failed.append((case_id, f"INVALID fraction sum: {result['verification'].fraction_sum}"))
        except Exception as e: failed.append((case_id, str(e)))
    print(f"Suite [{suite_name}]: {passed}/{len(cases)} passed.")
    return passed, failed

def main():
    # 1. Holistic Heirs (27 cases)
    holistic_27 = [{"id": f"T{i}", "heirs": {}} for i in range(1, 28)] # Placeholders, I'll fill key ones
    # (Mapping logic already validated in 92-case run, just expanding here)

    # 2. Grandparents (25 cases)
    gp_25 = [
        {"id": "G1", "heirs": {"PGF": 1, "PGM": 1}}, {"id": "G2", "heirs": {"MGF": 1, "MGM": 1}},
        {"id": "G3", "heirs": {"PGF": 1, "PGM": 1, "MGF": 1, "MGM": 1}},
        {"id": "G4", "heirs": {"PGF": 1, "PGM": 1, "MGF": 1}}, {"id": "G5", "heirs": {"PGF": 1, "PGM": 1, "MGM": 1}},
        {"id": "G6", "heirs": {"MGF": 1, "MGM": 1, "PGF": 1}}, {"id": "G7", "heirs": {"MGF": 1, "MGM": 1, "PGM": 1}},
        {"id": "G8", "heirs": {"PGF": 1}}, {"id": "G9", "heirs": {"MGF": 1}}, {"id": "G10", "heirs": {"PGM": 1}}, {"id": "G11", "heirs": {"MGM": 1}},
        {"id": "G12", "heirs": {"PGM": 3}}, {"id": "G13", "heirs": {"MGM": 2}},
        {"id": "G14", "heirs": {"PGM": 3, "MGM": 2}},
        {"id": "G15", "heirs": {"Father": 1, "PGM": 1}}, {"id": "G16", "heirs": {"Mother": 1, "MGM": 1}},
        {"id": "G17", "heirs": {"Father": 1, "Mother": 1, "PGM": 1}}, {"id": "G18", "heirs": {"Father": 1, "PGM": 1, "MGM": 1}},
        {"id": "G19", "heirs": {"PGF": 1, "Brother_maternal": 2}}, {"id": "G20", "heirs": {"PGF": 1, "Brother_maternal": 1}},
        {"id": "G21", "heirs": {"MGF": 1, "Brother": 2}},
        {"id": "G22", "heirs": {"PGF": 1, "Nephew": 1}}, {"id": "G23", "heirs": {"PGF": 1, "Nephew": 3}},
        {"id": "G24", "heirs": {"PGM": 3, "MGM": 2, "Daughter": 1}},
        {"id": "G25", "heirs": {"PGF": 1, "PGM": 1, "Brother": 1}}
    ]

    # 3. Children Descendants (16 cases)
    children_16 = [
        {"case_id": "C1", "heirs": [{"relation": "Son", "count": 1}, {"relation": "Daughter", "count": 1}]},
        {"case_id": "C2", "heirs": [{"relation": "Son", "count": 1}]},
        {"case_id": "C3", "heirs": [{"relation": "Daughter", "count": 1}]},
        {"case_id": "C4", "heirs": [{"relation": "Daughter", "count": 2}]},
        {"case_id": "C5", "heirs": [{"relation": "Daughter", "count": 1}, {"relation": "Daughter_of_Son", "count": 1}]},
        {"case_id": "C6", "heirs": [{"relation": "Daughter", "count": 1}, {"relation": "Son_of_Son", "count": 1}]},
        {"case_id": "C7", "heirs": [{"relation": "Son", "count": 1}, {"relation": "Father", "count": 1}]},
        {"case_id": "C8", "heirs": [{"relation": "Son_of_Son", "count": 1}, {"relation": "Daughter_of_Son", "count": 1}]},
        {"case_id": "C9", "heirs": [{"relation": "Son_of_Son", "count": 1}]},
        {"case_id": "C10", "heirs": [{"relation": "Daughter_of_Son", "count": 1}]},
        {"case_id": "C11", "heirs": [{"relation": "Daughter_of_Son", "count": 2}]},
        {"case_id": "C12", "heirs": [{"relation": "Daughter", "count": 1}, {"relation": "Son_of_Son", "count": 1}, {"relation": "Daughter_of_Son", "count": 1}]},
        {"case_id": "C13", "heirs": [{"relation": "Father", "count": 1}, {"relation": "Son_of_Son", "count": 1}]},
        {"case_id": "C14", "heirs": [{"relation": "Son_of_Son", "count": 1}]},
        {"case_id": "C15", "heirs": [{"relation": "Son_of_Son", "count": 1}, {"relation": "Son_of_Daughter", "count": 1}]},
        {"case_id": "C16", "heirs": [{"relation": "Daughter_of_Son", "count": 1}, {"relation": "Son_of_Daughter", "count": 1}]}
    ]

    # 4. Holistic (27 cases)
    holistic_27 = [
        {"id": "T1", "heirs": {"Father":1,"Mother":1}}, {"id": "T2", "heirs":{"Father":1,"Mother":1,"Son":1}},
        {"id": "T3", "heirs":{"Father":1,"Mother":1,"Son":1,"Daughter":1}}, {"id": "T4", "heirs":{"Father":1,"Mother":1,"Daughter":1}},
        {"id": "T5", "heirs":{"Mother":1,"Daughter":1}}, {"id": "T6", "heirs":{"Father":1,"Daughter":1}},
        {"id": "T7", "heirs":{"Father":1,"Mother":1, "Brother": 2}}, {"id": "T8", "heirs":{"Father":1,"Mother":1,"Brother_maternal":2}},
        {"id": "T9", "heirs":{"Mother":1,"Brother":2}}, {"id": "T10", "heirs":{"Husband":1}}, {"id": "T11", "heirs":{"Wife":1}},
        {"id": "T12", "heirs":{"Husband":1,"Son":1}}, {"id": "T13", "heirs":{"Wife":1,"Son":1}},
        {"id": "T14", "heirs":{"Wife":1,"Father":1,"Mother":1}}, {"id": "T15", "heirs":{"Husband":1,"Father":1,"Mother":1}},
        {"id": "T16", "heirs":{"Sister":1}}, {"id": "T17", "heirs":{"Sister":2}}, {"id": "T18", "heirs":{"Brother":1,"Sister":1}},
        {"id": "T19", "heirs":{"Brother_maternal":1}}, {"id": "T20", "heirs":{"Brother_maternal":2}},
        {"id": "T21", "heirs":{"Brother":1,"Brother_maternal":1}}, {"id": "T22", "heirs":{"Brother":1,"Sister_maternal":1}},
        {"id": "T23", "heirs":{"Grandfather_paternal":1,"Brother":1}}, {"id": "T24", "heirs":{"Grandfather_paternal":1,"Nephew":1}},
        {"id": "T25", "heirs":{"Grandfather_paternal":1,"Grandmother_paternal":1}},
        {"id": "T26", "heirs":{"Grandfather_paternal":1,"Grandmother_paternal":1,"Grandfather_maternal":1,"Grandmother_maternal":1}},
        {"id": "T27", "heirs":{"Grandmother":1}}
    ]

    # 5. Spouses (4 cases)
    spouses_4 = [{"case_id": "F1", "heirs": {"Wife": 1}}, {"case_id": "F2", "heirs": {"Husband": 1}}, {"case_id": "F3", "heirs": {}}, {"case_id": "F4", "heirs": {}}]

    # 6. Parent + Child (6 cases)
    parent_child_6 = [
        {"case_id": "H1", "heirs": {"Husband": 1, "Son": 6}}, {"case_id": "H2", "heirs": {"Husband": 1, "Son": 5}},
        {"case_id": "H3", "heirs": {"Husband": 1, "Sister": 5, "Grandfather_paternal": 1}},
        {"case_id": "H4", "heirs": {"Daughter": 1, "Father": 1}},
        {"case_id": "H5", "heirs": {"Husband": 1, "Daughter": 1, "Father": 1}},
        {"case_id": "H6", "heirs": {"Wife": 1, "Daughter": 20, "Father": 1}}
    ]

    # 7. Arham (8 cases)
    arham_8 = [
        {"id": "A1", "heirs": {"Aunt_paternal": 1, "Aunt_maternal": 1}},
        {"id": "A2", "heirs": {"Uncle_paternal": 1, "Aunt_paternal": 1, "Uncle_maternal": 1, "Aunt_maternal": 1}},
        {"id": "A3", "heirs": {"Son_of_maternal_uncle": 1, "Uncle_paternal": 1, "Aunt_paternal": 1}},
        {"id": "A4", "heirs": {"Cousin_paternal": 2, "Uncle_maternal": 1, "Aunt_maternal": 1}},
        {"id": "A5", "heirs": {"Son_of_aunt": 1, "Daughter_of_uncle": 1}},
        {"id": "A7", "heirs": {"Son": 1, "Son_of_Son": 1}}, {"id": "A8", "heirs": {"Daughter": 1, "Uncle_paternal": 1}}
    ]

    # 8. Core Rules (16 cases)
    core_16 = [
        {"id": "CR1", "heirs": {"Son": 1, "Daughter": 1}}, {"id": "CR2", "heirs": {"Son": 2}},
        {"id": "CR3", "heirs": {"Son": 1}}, {"id": "CR4", "heirs": {"Daughter": 2}},
        {"id": "CR5", "heirs": {"Daughter": 1}}, {"id": "CR6", "heirs": {"Father": 1, "Mother": 1}},
        {"id": "CR7", "heirs": {"Father": 1, "Mother": 1, "Son": 1}}, {"id": "CR8", "heirs": {"Father": 1, "Mother": 1, "Daughter": 1}},
        {"id": "CR9", "heirs": {"Father": 1, "Daughter": 1}}, {"id": "CR10", "heirs": {"Mother": 1, "Daughter": 1}},
        {"id": "CR11", "heirs": {"Father": 1, "Mother": 1, "Brother": 2}}, {"id": "CR12", "heirs": {"Father": 1, "Mother": 1, "Brother_maternal": 2}},
        {"id": "CR13", "heirs": {"Husband": 1}}, {"id": "CR14", "heirs": {"Husband": 1, "Son": 1}},
        {"id": "CR15", "heirs": {"Wife": 1}}, {"id": "CR16", "heirs": {"Wife": 1, "Son": 1}}
    ]

    # 9. Final 25 Holistic
    final_25 = [
        {"id":"F1","heirs":{"Grandson":1,"Father":1}}, {"id":"F2","heirs":{"Granddaughter":1,"Father":1}},
        {"id":"F3","heirs":{"DaughtersSon":1,"Father":1}}, {"id":"F4","heirs":{"Wife":1,"Father":1,"Mother":1,"Grandmother":1,"Son":1}},
        {"id":"F5","heirs":{"Husband":1,"Grandson":1,"Granddaughter":1}}, {"id":"F6","heirs":{"Husband":1,"Father":1,"Mother":1}},
        {"id":"F7","heirs":{"MaternalSibling":2}}, {"id":"F8","heirs":{"MaternalSibling":1}},
        {"id":"F9","heirs":{"MaternalNephews":2, "FullNephews":3}}, {"id":"F10","heirs":{"Grandfather":1,"Nephew":1}},
        {"id":"F11","heirs":{"Grandfather":1,"MaternalSiblings":2}}, {"id":"F12","heirs":{"Grandfather":1,"MaternalSibling":1}},
        {"id":"F13","heirs":{"MaternalGrandfather":1,"PaternalSiblings":2}}, {"id":"F14","heirs":{"Grandmothers":2,"Nephew":1}},
        {"id":"F15","heirs":{"GrandmotherMaternal":1,"GrandmotherPaternal":1,"Daughter":1}},
        {"id":"F16","heirs":{"Grandmother":1,"Father":1,"Mother":1,"Siblings":2}},
        {"id":"F17","heirs":{"Grandmother":1,"Grandfather":1,"BrotherFull":1,"BrotherPaternal":1}},
        {"id":"F18","heirs":{"Grandmother":1,"Brother":1}}, {"id":"F19","heirs":{"FullAunt":1,"MaternalAunt":1}},
        {"id":"F20","heirs":{"MaternalUncle":1,"MaternalAunt":1,"PaternalUncle":1,"PaternalAunt":1}},
        {"id":"F21","heirs":{"MaternalGrandfather":1,"MaternalUncle":1,"MaternalAunt":1}}, {"id":"F22","heirs":{"MaternalUncle":1,"MaternalAunt":1}},
        {"id":"F23","heirs":{"PaternalAunt":1,"MaternalAunt":1}}, {"id":"F24","heirs":{"PaternalUncle":1,"BrothersGranddaughter":1}},
        {"id":"F25","heirs":{"MaternalUncle":1,"SistersSon":1}}
    ]

    suites = [
        ("GP 25", gp_25), ("Children 16", children_16), ("Holistic 27", holistic_27),
        ("Spouses 4", spouses_4), ("Parent+Child 6", parent_child_6), ("Arham 8", arham_8),
        ("Core 16", core_16), ("Final 25", final_25)
    ]
    
    tp, tc = 0, 0
    for name, cases in suites:
        p, f = run_test_suite(name, cases)
        tp += p
        tc += len(cases)
        for f_id, f_msg in f: print(f"  FAILED [{name}] {f_id}: {f_msg}")
    print(f"\nGRAND TOTAL: {tp}/{tc} PASSED")

if __name__ == "__main__": main()
