from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any, Set, Union
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

class BlockingDetail(BaseModel):
    blocked: bool = False
    blocked_by: Optional[str] = None
    blocking_rule: Optional[str] = None
    arabic_text: Optional[str] = None

class IndividualHeir(BaseModel):
    heir_id: str # e.g. Daughter_1
    relation: str
    fraction: Fraction
    amount: Fraction
    blocking: Optional[BlockingDetail] = None
    
    class Config:
        arbitrary_types_allowed = True

class RuleCondition(BaseModel):
    fact: str # count, exists, has_male, has_female, is_killer, etc.
    relation: Optional[str] = None
    target_class: Optional[str] = None # For class-based checks
    operator: str # ==, >=, >, <, <=, !=
    value: Any

class RuleAction(BaseModel):
    type: str # assign_fraction, assign_remainder, exclude_heir, mark_blocked, flag_radd, substitute_relation, procedure_action, blocking
    target: Optional[str] = None
    value: Optional[str] = None # For fraction strings like "1/2"
    radd_eligible: bool = False
    source: Optional[str] = None # For substitution
    as_relation: Optional[str] = None # For substitution (using 'as_relation' because 'as' is reserved)

class Rule(BaseModel):
    rule_id: str
    priority: int
    category: str # eligibility, substitution, exclusion, allocation, final, blocking
    slot: Optional[str] = None # logical slot to prevent overwrites (e.g., descendant_fixed)
    conditions: Dict[str, List[RuleCondition]] # "all", "any", "none"
    actions: List[RuleAction]
    arabic_text: str
    meaning: str

class CaseState(BaseModel):
    estate_total: Fraction = Field(default=Fraction(0))
    debts: Fraction = Field(default=Fraction(0))
    wasiyyah: Fraction = Field(default=Fraction(0))
    heirs: List[Heir]
    valid_heirs: List[Heir] = []
    
    # Decisions Ledger
    assigned_fractions: Dict[str, Fraction] = {} # relation -> fraction
    radd_pool: Set[str] = set() # relations eligible for radd
    remainder_sink: Optional[str] = None # primary relation to take leftover
    excluded_relations: Set[str] = set() # relations blocked by proximity or other rules
    blocking_map: Dict[str, BlockingDetail] = {} # relation -> blocking details
    virtual_mappings: Dict[str, str] = {} # substituted relations (e.g., Grandson -> Son)
    
    # Verification Ledger
    individual_results: List[IndividualHeir] = []
    
    # Tracking
    fired_rules: List[str] = []
    occupied_slots: Set[str] = set()
    
    class Config:
        arbitrary_types_allowed = True

class VerificationData(BaseModel):
    estate_total: float
    total_distributed: float
    fraction_sum: str
    status: str # VALID or INVALID

class CalculationResult(BaseModel):
    heir_id: str
    relation: str
    share: str 
    amount: float
    rules_used: List[str]
    arabic_reasoning: List[str]
    is_blocked: bool = False
    blocked_by: Optional[str] = None
    blocking_rule_id: Optional[str] = None

class CalculationRequest(BaseModel):
    estate_value: float
    debts: float = 0.0
    wasiyyah: float = 0.0
    heirs: List[Heir]

class CalculationResponse(BaseModel):
    case_id: int
    results: List[CalculationResult]
    verification: VerificationData
