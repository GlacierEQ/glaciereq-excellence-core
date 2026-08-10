from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(slots=True)
class EvidencePacket:
    source: str
    content_hash: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ClaimReceipt:
    claim_id: str
    subject: str
    status: str
    evidence: List[EvidencePacket] = field(default_factory=list)
    notes: Optional[str] = None


@dataclass(slots=True)
class EnvelopeContract:
    contract_id: str
    producer: str
    consumer: str
    schema_version: str
    constraints: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class AuthorityMatrix:
    object_type: str
    roles: Dict[str, List[str]] = field(default_factory=dict)

    def allows(self, role: str, action: str) -> bool:
        return action in self.roles.get(role, [])


@dataclass(slots=True)
class QuorumVote:
    vote_id: str
    threshold: int
    approvals: List[str] = field(default_factory=list)

    def passed(self) -> bool:
        return len(self.approvals) >= self.threshold
