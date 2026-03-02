import sys
import os
from fractions import Fraction

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.engine.core import EnginePipeline
from app.engine.models import Heir

def test_radd_fix():
    pipeline = EnginePipeline()
    
    # Case 1: Father + Son_of_Daughter
    # Estate = 40000
    heirs = [
        Heir(relation="Father", relation_type="Father", lineage="direct", gender="M", count=1),
        Heir(relation="Son of Daughter", relation_type="Son_of_Daughter", lineage="maternal_descendant", gender="M", count=1)
    ]
    
    result = pipeline.calculate(heirs, 40000)
    
    print("Case 1: Father + Son_of_Daughter")
    for r in result["results"]:
        print(f"Heir: {r.relation}, Share: {r.share}, Amount: {r.amount}")
    
    father = next(r for r in result["results"] if r.relation == "Father")
    son_daughter = next(r for r in result["results"] if r.relation == "Son of Daughter")
    
    assert father.share == "1/6", f"Expected Father share 1/6, got {father.share}"
    assert son_daughter.share == "5/6", f"Expected Son_of_Daughter share 5/6, got {son_daughter.share}"
    assert father.amount == 6666.67, f"Expected Father amount 6666.67, got {father.amount}"
    
    print("\nCase 2: Father + Daughter_of_Daughter")
    heirs2 = [
        Heir(relation="Father", relation_type="Father", lineage="direct", gender="M", count=1),
        Heir(relation="Daughter of Daughter", relation_type="Daughter_of_Daughter", lineage="maternal_descendant", gender="F", count=1)
    ]
    result2 = pipeline.calculate(heirs2, 40000)
    for r in result2["results"]:
        print(f"Heir: {r.relation}, Share: {r.share}, Amount: {r.amount}")
    
    print("\nAll checks passed!")

if __name__ == "__main__":
    test_radd_fix()
