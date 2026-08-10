"""
GlacierEQ Excellence Core - Layer 1 Primitive & Protocol Engine
Location: /data/data/com.termux/files/home/EXCELLENCE_PACKS/glaciereq-excellence-core/src/glaciereq_excellence_core
"""
from __future__ import annotations

import hashlib
import json
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Type, TypeVar
import jsonschema
from pydantic import BaseModel, Field

# ==========================================
# 1. PROTOCOL VERSIONING ENGINE
# ==========================================

@dataclass(frozen=True)
class ProtocolVersion:
    major: int
    minor: int
    patch: int

    @property
    def semver(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    @classmethod
    def parse(cls, semver: str) -> ProtocolVersion:
        parts = semver.strip().split(".")
        if len(parts) != 3:
            raise ValueError(f"Invalid SemVer string format: {semver!r}. Expected 'X.Y.Z'")
        try:
            return cls(major=int(parts[0]), minor=int(parts[1]), patch=int(parts[2]))
        except ValueError as err:
            raise ValueError(f"Non-integer SemVer component in {semver!r}") from err

    def is_compatible_with(self, target: ProtocolVersion) -> bool:
        """Major versions must match; artifact minor must be <= consumer minor."""
        return self.major == target.major and target.minor <= self.minor

    def assert_compatible(self, semver_str: str) -> None:
        target = ProtocolVersion.parse(semver_str)
        if not self.is_compatible_with(target):
            raise ValueError(
                f"Protocol Version Incompatible! Consumer={self.semver}, Payload={semver_str}. "
                "Execution rejected to prevent state corruption."
            )

CURRENT_VERSION = ProtocolVersion(major=1, minor=0, patch=0)

# ==========================================
# 2. CORE DATA MODELS (Pydantic v2)
# ==========================================

class EvidencePacket(BaseModel):
    source: str = Field(..., min_length=1)
    content_hash: str = Field(..., min_length=8)
    timestamp: float = Field(default_factory=time.time)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def create(cls, source: str, raw_bytes: bytes, metadata: Optional[Dict[str, Any]] = None) -> EvidencePacket:
        digest = hashlib.sha256(raw_bytes).hexdigest()
        return cls(source=source, content_hash=f"sha256:{digest}", metadata=metadata or {})


class ClaimReceipt(BaseModel):
    claim_id: str = Field(..., min_length=1)
    subject: str = Field(..., min_length=1)
    status: str = Field(..., pattern="^(open|closed|pending|rejected|verified)$")
    evidence: List[EvidencePacket] = Field(default_factory=list)
    notes: Optional[str] = None

    def add_evidence(self, packet: EvidencePacket) -> None:
        self.evidence.append(packet)


class EnvelopeContract(BaseModel):
    contract_id: str = Field(..., min_length=1)
    producer: str = Field(..., min_length=1)
    consumer: str = Field(..., min_length=1)
    schema_version: str = Field(..., pattern=r"^\d+\.\d+\.\d+$")
    constraints: Dict[str, Any] = Field(default_factory=dict)


class AuthorityMatrix(BaseModel):
    object_type: str = Field(..., min_length=1)
    roles: Dict[str, List[str]] = Field(default_factory=dict)

    def allows(self, role: str, action: str) -> bool:
        allowed_actions = self.roles.get(role, [])
        return action in allowed_actions or "*" in allowed_actions


class QuorumVote(BaseModel):
    vote_id: str = Field(..., min_length=1)
    threshold: int = Field(..., ge=1)
    approvals: List[str] = Field(default_factory=list)

    def add_approval(self, approver_id: str) -> bool:
        if approver_id not in self.approvals:
            self.approvals.append(approver_id)
        return self.passed()

    def passed(self) -> bool:
        return len(set(self.approvals)) >= self.threshold

# ==========================================
# 3. SCHEMA VALIDATION ENGINE
# ==========================================

CLAIM_SCHEMA: Dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "required": ["claim_id", "subject", "status"],
    "properties": {
        "claim_id": {"type": "string", "minLength": 1},
        "subject": {"type": "string", "minLength": 1},
        "status": {"type": "string", "enum": ["open", "closed", "pending", "rejected", "verified"]},
        "evidence": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["source", "content_hash"],
                "properties": {
                    "source": {"type": "string"},
                    "content_hash": {"type": "string"},
                    "timestamp": {"type": "number"},
                    "metadata": {"type": "object"}
                }
            }
        },
        "notes": {"type": ["string", "null"]}
    },
    "additionalProperties": False
}

ENVELOPE_SCHEMA: Dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "required": ["contract_id", "producer", "consumer", "schema_version"],
    "properties": {
        "contract_id": {"type": "string", "minLength": 1},
        "producer": {"type": "string"},
        "consumer": {"type": "string"},
        "schema_version": {"type": "string", "pattern": r"^\d+\.\d+\.\d+$"},
        "constraints": {"type": "object"}
    },
    "additionalProperties": False
}

def validate_payload(payload: Dict[str, Any], schema: Dict[str, Any]) -> None:
    """Validate untrusted input dict against JSON Schema. Raises ValidationError if invalid."""
    jsonschema.validate(instance=payload, schema=schema)

# ==========================================
# 4. SERIALIZATION / DESERIALIZATION
# ==========================================

T = TypeVar("T", bound=BaseModel)

def serialize(obj: BaseModel) -> str:
    """Serialize Pydantic model into protocol-enveloped JSON string with checksum."""
    data_dict = obj.model_dump()
    serialized_bytes = json.dumps(data_dict, sort_keys=True).encode("utf-8")
    checksum = hashlib.sha256(serialized_bytes).hexdigest()
    
    envelope = {
        "_protocol_version": CURRENT_VERSION.semver,
        "_type": type(obj).__name__,
        "_checksum": f"sha256:{checksum}",
        "data": data_dict,
    }
    return json.dumps(envelope, indent=2)


def deserialize(raw: str, model_cls: Type[T]) -> T:
    """Deserialize JSON string into target Pydantic model with strict version/checksum checks."""
    envelope = json.loads(raw)
    embedded_ver = envelope.get("_protocol_version", "0.0.0")
    CURRENT_VERSION.assert_compatible(embedded_ver)
    
    # Optional checksum verification if present
    checksum = envelope.get("_checksum")
    if checksum:
        data_bytes = json.dumps(envelope["data"], sort_keys=True).encode("utf-8")
        calc_hash = f"sha256:{hashlib.sha256(data_bytes).hexdigest()}"
        if checksum != calc_hash:
            raise ValueError(f"Checksum corruption detected! Expected {checksum}, got {calc_hash}")

    return model_cls(**envelope["data"])

# ==========================================
# 5. BASE MODULE ABSTRACT CONTRACT
# ==========================================

class BaseModule(ABC):
    name: str = "unnamed-module"
    version: str = "0.1.0"

    @abstractmethod
    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Execute core logic. Must return {'status': 'ok'|'error', 'result': ...}."""
        raise NotImplementedError

    def healthcheck(self) -> Dict[str, Any]:
        """Return non-blocking health check telemetry."""
        return {
            "module": self.name,
            "version": self.version,
            "protocol_version": CURRENT_VERSION.semver,
            "status": "ok",
        }
