from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from ..database.session import get_db
from ..database.schema import CaseRecord, ResultRecord
from ..engine.core import EnginePipeline
from ..engine.models import Heir, CalculationResult
from pydantic import BaseModel

router = APIRouter()
engine = EnginePipeline()

class CalculationRequest(BaseModel):
    estate_value: float
    debts: float = 0.0
    wasiyyah: float = 0.0
    heirs: List[Heir]

@router.post("/calculate")
def calculate_inheritance(req: CalculationRequest, db: Session = Depends(get_db)):
    try:
        # 1. Run the Jurisprudence Engine
        results = engine.calculate(req.heirs, req.estate_value, req.debts, req.wasiyyah)
        
        # 2. Persist the Case
        new_case = CaseRecord(
            estate_value=req.estate_value,
            heirs_input=[h.dict() for h in req.heirs]
        )
        db.add(new_case)
        db.commit()
        db.refresh(new_case)
        
        # 3. Persist the Results
        persistent_results = []
        for res in results:
            new_result = ResultRecord(
                case_id=new_case.id,
                heir_relation=res["heir"],
                share_fraction=res["share"],
                amount=res["amount"],
                rules_used=res["rules_used"],
                arabic_reasoning=res["arabic_reasoning"]
            )
            db.add(new_result)
            persistent_results.append(res)
        
        db.commit()
        
        return {
            "case_id": new_case.id,
            "results": persistent_results
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

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
                "heir": r.heir_relation,
                "share": r.share_fraction,
                "amount": r.amount,
                "rules_used": r.rules_used,
                "arabic_reasoning": r.arabic_reasoning
            } for r in case.results
        ]
    }
