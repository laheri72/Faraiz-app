
from backend.app.engine.core import EnginePipeline
from backend.app.engine.models import Heir
import json

def test_case():
    heirs = [
        Heir(relation="Mother", relation_type="Mother", lineage="direct", gender="F", count=1),
        Heir(relation="Wife", relation_type="Wife", lineage="direct", gender="F", count=1),
        Heir(relation="Paternal Grandfather", relation_type="grandfather_paternal", lineage="paternal", gender="M", count=1, generation_level=2),
        Heir(relation="Maternal Grandfather", relation_type="grandfather_maternal", lineage="maternal", gender="M", count=1, generation_level=2),
        Heir(relation="Maternal Grandmother", relation_type="grandmother_maternal", lineage="maternal", gender="F", count=1, generation_level=2),
        Heir(relation="Full Sister", relation_type="Sister", lineage="paternal", gender="F", count=3),
        Heir(relation="Maternal Brother", relation_type="Brother_Maternal", lineage="maternal", gender="M", count=1),
        Heir(relation="Maternal Sister", relation_type="Sister_Maternal", lineage="maternal", gender="F", count=1),
    ]
    
    pipeline = EnginePipeline()
    result = pipeline.calculate(heirs, 1000)
    
    # Correctly serialize Pydantic models
    def serialize_pydantic(obj):
        if isinstance(obj, list):
            return [serialize_pydantic(i) for i in obj]
        if hasattr(obj, "model_dump"):
            return obj.model_dump()
        if hasattr(obj, "dict"):
            return obj.dict()
        return obj

    serializable_result = {
        "results": serialize_pydantic(result["results"]),
        "verification": serialize_pydantic(result["verification"])
    }
    
    print(json.dumps(serializable_result, indent=2))

if __name__ == "__main__":
    test_case()
