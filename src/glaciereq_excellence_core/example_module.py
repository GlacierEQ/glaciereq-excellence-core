"""Worked example: NullGateModule

This module demonstrates the full BaseModule contract end-to-end.
Downstream excellence packs should follow this exact pattern:

1. Subclass BaseModule.
2. Declare name and version.
3. Validate incoming payload against a schema before processing.
4. Return a ClaimReceipt (or other core model) serialized via serialize().

Copy this file into your pack repo as a starting template.
"""
from __future__ import annotations
from typing import Any, Dict
from .base import BaseModule
from .models import ClaimReceipt, EvidencePacket
from .schema import validate_payload, CLAIM_SCHEMA
from .serialization import serialize


_INPUT_SCHEMA = {
    "type": "object",
    "required": ["claim_id", "subject"],
    "properties": {
        "claim_id": {"type": "string"},
        "subject": {"type": "string"},
    }
}


class NullGateModule(BaseModule):
    """A minimal gate module that accepts any claim and marks it pending.
    
    Use this as the starting scaffold for a new excellence pack module.
    Replace the run() body with real domain logic.
    """
    name = "null-gate"
    version = "0.1.0"

    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        validate_payload(payload, _INPUT_SCHEMA)

        evidence = EvidencePacket(
            source=self.name,
            content_hash="sha256:null",
            metadata={"input_keys": list(payload.keys())},
        )
        receipt = ClaimReceipt(
            claim_id=payload["claim_id"],
            subject=payload["subject"],
            status="pending",
            evidence=[evidence],
        )
        return {
            "status": "ok",
            "result": serialize(receipt),
        }
