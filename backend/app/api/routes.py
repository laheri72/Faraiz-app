import json
import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from ..database.session import get_db
from ..database.schema import CaseRecord, ResultRecord
from ..engine.core import EnginePipeline, KNOWLEDGE_BASE
from ..engine.models import Heir, CalculationResponse, CalculationRequest

router = APIRouter()
engine = EnginePipeline()

@router.get("/rules")
def get_rules():
    try:
        # Return the actual rules used by the engine
        return [rule.model_dump() for rule in KNOWLEDGE_BASE]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/calculate", response_model=CalculationResponse)
def calculate_inheritance(req: CalculationRequest, db: Session = Depends(get_db)):
    print(f"\n>>> RECEIVED REQUEST: Estate={req.estate_value}")
    try:
        # 1. Run the Jurisprudence Engine
        print(">>> STEP 1: Running Engine...")
        output = engine.calculate(req.heirs, req.estate_value, req.debts, req.wasiyyah)
        results = output["results"]
        verification = output["verification"]
        print(f">>> STEP 1 COMPLETE: {len(results)} heirs calculated.")
        
        # 2. Persist to Database
        print(">>> STEP 2: Saving to Database...")
        new_case = CaseRecord(
            estate_value=req.estate_value,
            heirs_input=[h.model_dump() for h in req.heirs]
        )
        db.add(new_case)
        db.flush() 
        print(f">>> STEP 2: Case ID {new_case.id} created. Saving results...")
        
        for res in results:
            new_result = ResultRecord(
                case_id=new_case.id,
                heir_relation=res.relation,
                share_fraction=res.share,
                amount=res.amount,
                rules_used=res.rules_used,
                arabic_reasoning=res.arabic_reasoning
            )
            db.add(new_result)
        
        db.commit()
        print(">>> STEP 3: Transaction committed.")
        
        # We skip refresh() to avoid potential hangs on some SQLite drivers
        # new_case.id is already available due to flush()
        
        return {
            "case_id": new_case.id,
            "results": results,
            "verification": verification,
            "calculation_steps": output.get("calculation_steps", [])
        }
    except ValueError as ve:
        print(f">>> INTEGRITY ERROR: {str(ve)}")
        db.rollback()
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        print(f">>> UNEXPECTED ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.get("/cases/{case_id}")
def get_case(case_id: int, db: Session = Depends(get_db)):
    case = db.query(CaseRecord).filter(CaseRecord.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    return {
        "id": case.id,
        "estate_value": case.estate_value,
        "heirs_input": case.heirs_input,
        "results": [
            {
                "heir_id": f"{r.heir_relation}_{i}",
                "relation": r.heir_relation,
                "share": r.share_fraction,
                "amount": r.amount,
                "rules_used": r.rules_used,
                "arabic_reasoning": r.arabic_reasoning
            } for i, r in enumerate(case.results)
        ]
    }
