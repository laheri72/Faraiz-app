import sys
import os
from fractions import Fraction

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.engine.models import Heir
from app.engine.core import EnginePipeline

def run_test(name, estate, heirs_list):
    engine = EnginePipeline()
    heirs = [Heir(**h) for h in heirs_list]
    
    print(f"\n--- TEST: {name} ---")
    print(f"Estate: {estate}")
    print(f"Heirs: {', '.join([f'{h.relation}({h.count})' for h in heirs])}")
    
    try:
        result = engine.calculate(heirs, estate)
        print("Results:")
        for res in result['results']:
            print(f"  Relation: {res.relation}, Share: {res.share}, Amount: {res.amount}")
        
        print("Verification:")
        print(f"  Status: {result['verification'].status}")
        print(f"  Fraction Sum: {result['verification'].fraction_sum}")
        print(f"  Total Distributed: {result['verification'].total_distributed}")
    except Exception as e:
        print(f"  ERROR: {e}")

def run_all_cases():
    # Case A: Father Mother Wife
    run_test("Case A: Father Mother Wife", 100000, [
        {"relation": "Father", "gender": "M", "count": 1},
        {"relation": "Mother", "gender": "F", "count": 1},
        {"relation": "Wife", "gender": "F", "count": 1}
    ])

    # Case B: Father Mother Wife Brother
    run_test("Case B: Father Mother Wife Brother", 100000, [
        {"relation": "Father", "gender": "M", "count": 1},
        {"relation": "Mother", "gender": "F", "count": 1},
        {"relation": "Wife", "gender": "F", "count": 1},
        {"relation": "Brother", "gender": "M", "count": 1}
    ])

    # Case C: Father Wife
    run_test("Case C: Father Wife", 100000, [
        {"relation": "Father", "gender": "M", "count": 1},
        {"relation": "Wife", "gender": "F", "count": 1}
    ])

    # Case D: Father Mother Son Daughter
    run_test("Case D: Father Mother Son Daughter", 100000, [
        {"relation": "Father", "gender": "M", "count": 1},
        {"relation": "Mother", "gender": "F", "count": 1},
        {"relation": "Son", "gender": "M", "count": 1},
        {"relation": "Daughter", "gender": "F", "count": 1}
    ])

if __name__ == "__main__":
    run_all_cases()
