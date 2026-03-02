from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .session import Base

class CaseRecord(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True)
    estate_value = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    heirs_input = Column(JSON, nullable=False) # raw list of heirs as input
    
    results = relationship("ResultRecord", back_populates="case")

class ResultRecord(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"))
    heir_relation = Column(String, nullable=False)
    share_fraction = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    rules_used = Column(JSON, nullable=False)
    arabic_reasoning = Column(JSON, nullable=False)

    case = relationship("CaseRecord", back_populates="results")
