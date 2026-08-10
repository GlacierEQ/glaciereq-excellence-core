from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional


class EvidencePacket(BaseModel):
    source: str
    content_hash: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ClaimReceipt(BaseModel):
    claim_id: str
    subject: str
    status: str
    evidence: List[EvidencePacket] = Field(default_factory=list)
    notes: Optional[str] = None


class EnvelopeContract(BaseModel):
    contract_id: str
    producer: str
    consumer: str
    schema_version: str
    constraints: Dict[str, Any] = Field(default_factory=dict)


class AuthorityMatrix(BaseModel):
    object_type: str
    roles: Dict[str, List[str]] = Field(default_factory=dict)

    def allows(self, role: str, action: str) -> bool:
        return action in self.roles.get(role, [])


class QuorumVote(BaseModel):
    vote_id: str
    threshold: int
    approvals: List[str] = Field(default_factory=list)

    def passed(self) -> bool:
        return len(self.approvals) >= self.threshold
