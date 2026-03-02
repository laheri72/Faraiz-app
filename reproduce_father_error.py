import sys
import os
from fractions import Fraction

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.engine.models import Heir
from app.engine.core import EnginePipeline

def run_test_case():
    engine = EnginePipeline()
    
    # Case: Estate = 100000
    # Heirs: Father=1, Mother=1, Wife=1, Brother=1
    heirs = [
        Heir(relation="Father", gender="M", count=1),
        Heir(relation="Mother", gender="F", count=1),
        Heir(relation="Wife", gender="F", count=1),
        Heir(relation="Brother", gender="M", count=1)
    ]
    
    estate = 100000
    
    print(f"Running calculation for Estate: {estate}")
    
    result = engine.calculate(heirs, estate)
    
    print("\nResults:")
    for res in result['results']:
        print(f"Relation: {res.relation}, Share: {res.share}, Amount: {res.amount}")
    
    print("\nVerification:")
    print(f"Status: {result['verification'].status}")
    print(f"Fraction Sum: {result['verification'].fraction_sum}")
    print(f"Total Distributed: {result['verification'].total_distributed}")

if __name__ == "__main__":
    run_test_case()
