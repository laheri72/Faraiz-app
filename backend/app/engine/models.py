from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any, Set
from fractions import Fraction

class Heir(BaseModel):
    relation: str  # e.g., "Son", "Daughter", "Husband", "Mother"
    gender: str    # "M" or "F"
    count: int = 1

class Rule(BaseModel):
    rule_id: str
    arabic_text: str
    meaning: str
    conditions: Dict[str, Any]
    actions: Dict[str, Any]
    priority: int
    source: str

class CaseState(BaseModel):
    estate_total: Fraction = Field(default=Fraction(1, 1))
    heirs: List[Heir]
    valid_heirs: List[Heir] = []
    excluded_heirs: List[str] = []
    assignments: Dict[str, Fraction] = {} # heir relation -> fraction
    applied_rules: List[str] = []
    radd_eligible: List[str] = [] # list of relation names eligible for radd
    
    class Config:
        arbitrary_types_allowed = True

class CalculationResult(BaseModel):
    heir: str
    share: str  # fraction as string e.g. "1/6"
    amount: float
    rules_used: List[str]
    arabic_reasoning: List[str]
