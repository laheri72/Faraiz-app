import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.engine.core import EnginePipeline
from app.engine.models import Heir

def run_test(name, estate, heirs):
    print(f"\n[VALIDATION] {name}")
    pipeline = EnginePipeline()
    results = pipeline.calculate(heirs, estate, debts=0, wasiyyah=0)
    
    for res in results:
        print(f"  - {res['heir']}: Share {res['share']}, Amount {res['amount']}")
    return results

if __name__ == "__main__":
    print("=== FATEMI WIRASAT ENGINE: PHASE 5 VALIDATION ===")
    
    # Validation 1: Sibling Blocking (Principle 1 & Rule V14)
    # Father should block Brother
    run_test("V14: Sibling Blocking (Father vs Brother)", 100000, [
        Heir(relation="Father", gender="M", count=1),
        Heir(relation="Brother", gender="M", count=1)
    ])

    # Validation 2: Gender Ratio (Principle 3 & Rule V1)
    # Son should get 2x Daughter
    run_test("V1: Gender Ratio (Son + Daughter)", 300000, [
        Heir(relation="Son", gender="M", count=1),
        Heir(relation="Daughter", gender="F", count=1)
    ])

    # Validation 3: Grandchildren Substitution (Principle 5 & Rule V6)
    # Grandson should act as Son
    # Note: Need to ensure Grandson is in rules.json or handled by substitution logic
    run_test("V6: Substitution (Grandson Only)", 100000, [
        Heir(relation="Grandson", gender="M", count=1)
    ])

    # Validation 4: Quranic Fixed Shares (Rule V9 & V12)
    # Husband (1/4) + Mother (1/6) + Son (Remainder)
    run_test("V9/V12: Fixed Shares with Children", 240000, [
        Heir(relation="Husband", gender="M", count=1),
        Heir(relation="Mother", gender="F", count=1),
        Heir(relation="Son", gender="M", count=1)
    ])
