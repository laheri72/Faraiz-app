import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.engine.pipeline import EnginePipeline
from app.engine.models import Heir

def run_test(name, estate, heirs):
    print(f"\n--- Running {name} ---")
    print(f"Estate: {estate}")
    print(f"Heirs: {[(h.relation, h.count) for h in heirs]}")
    
    pipeline = EnginePipeline()
    results = pipeline.calculate(heirs, estate)
    
    for res in results:
        print(f"Heir: {res['heir']} | Share: {res['share']} | Amount: {res['amount']}")
        # print(f"Rules: {res['rules_used']}")

# TEST1: Estate 240,000 | Wife, Mother, 2 daughters
# In Daim al-Islam: 
# Wife gets 1/8 (with children)
# Mother gets 1/6 (with children)
# 2 daughters get fixed shares (2/3) then Radd
test1_heirs = [
    Heir(relation="Wife", gender="F", count=1),
    Heir(relation="Mother", gender="F", count=1),
    Heir(relation="Daughter", gender="F", count=2)
]
# Wait, my rules.json needs V4 for 'two daughters'
# Let me add V4 and others to rules.json before running

# TEST2: Estate 100,000 | Single son
test2_heirs = [Heir(relation="Son", gender="M", count=1)]

# TEST3: Estate 120,000 | Father, Mother
test3_heirs = [
    Heir(relation="Father", gender="M", count=1),
    Heir(relation="Mother", gender="F", count=1)
]

# TEST4: Estate 90,000 | Single daughter
test4_heirs = [Heir(relation="Daughter", gender="F", count=1)]

if __name__ == "__main__":
    run_test("TEST1: Complex Case", 240000, test1_heirs)
    run_test("TEST2: Single Son", 100000, test2_heirs)
    run_test("TEST4: Single Daughter", 90000, test4_heirs)
    run_test("TEST3: Parents Only", 120000, test3_heirs)
