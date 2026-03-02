from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any, Set
from fractions import Fraction

class Heir(BaseModel):
    relation: str  # e.g., "Son", "Daughter", "Husband", "Mother", "Brother", "Sister", "Uncle", "Cousin", "Dhawu_Arham"
    gender: str    # "M" or "F"
    count: int = 1
    # Special conditions (Layer 4)
    is_killer: bool = False
    is_different_religion: bool = False
    is_illegitimate: bool = False
    is_missing: bool = False

class Rule(BaseModel):
    rule_id: str
    arabic_text: str
    meaning: str

class CaseState(BaseModel):
    estate_total: float = 0.0
    debts: float = 0.0
    wasiyyah: float = 0.0
    heirs: List[Heir]
    valid_heirs: List[Heir] = []
    excluded_heirs: List[str] = [] # specific relation names excluded
    assignments: Dict[str, Fraction] = {} # heir relation -> fraction
    applied_rules: List[str] = []
    radd_eligible: List[str] = [] 
    
    class Config:
        arbitrary_types_allowed = True

class CalculationResult(BaseModel):
    heir: str
    count: int = 1
    share: str  # fraction as string e.g. "1/6"
    amount: float
    rules_used: List[str]
    arabic_reasoning: List[str]
