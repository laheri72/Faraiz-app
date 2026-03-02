import sys
import os
from fractions import Fraction
sys.path.append(os.path.dirname(__file__))

from backend.app.engine.core import EnginePipeline
from backend.app.engine.models import Heir

def reproduce_issue():
    pipeline = EnginePipeline()
    # Data from user's payload
    heirs = [
        Heir(relation="Son", gender="M", count=2),
        Heir(relation="Daughter", gender="F", count=1),
        Heir(relation="Father", gender="M", count=1)
    ]
    estate = 100000
    
    print("Reproducing calculation with User Data...")
    try:
        output = pipeline.calculate(heirs, estate, 0, 0)
        print("Calculation complete successfully!")
        print(f"Heirs in result: {len(output['results'])}")
        for r in output['results']:
            print(f" - {r.heir_id}: {r.share} -> {r.amount}")
        print(f"Status: {output['verification'].status}")
    except Exception as e:
        print(f"CRASH DETECTED: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    reproduce_issue()
