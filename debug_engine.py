import sys
import os
from fractions import Fraction
sys.path.append(os.path.dirname(__file__))

from backend.app.engine.core import EnginePipeline
from backend.app.engine.models import Heir

def test_engine():
    pipeline = EnginePipeline()
    heirs = [
        Heir(relation="Father", gender="M", count=1),
        Heir(relation="Mother", gender="F", count=1),
        Heir(relation="Son", gender="M", count=1)
    ]
    estate = 72000
    
    print("Starting calculation...")
    try:
        output = pipeline.calculate(heirs, estate)
        print("Calculation complete.")
        print(f"Results: {len(output['results'])} heirs")
        print(f"Verification: {output['verification'].status}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_engine()
