from pydantic import BaseModel
from typing import List, Optional

class ClaimRequest(BaseModel):
    claim: str
    pdf_text: Optional[str] = None

class AnalysisResponse(BaseModel):
    analysis: str
    risk_level: str
    search_results: List[dict]

class LedgerEntry(BaseModel):
    id: int
    claim: str
    result: str
    hash: str
    risk_level: str
    timestamp: str

class ReportRequest(BaseModel):
    claims: List[dict]
