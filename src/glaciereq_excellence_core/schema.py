"""JSON Schema validation for excellence pack payloads.

All packs should call validate_payload() on untrusted input before
deserializing it into a model. This provides a second layer of defense
beyond Pydantic's own field validation.
"""
from __future__ import annotations
from typing import Any, Dict
import jsonschema


CLAIM_SCHEMA: Dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "required": ["claim_id", "subject", "status"],
    "properties": {
        "claim_id": {"type": "string", "minLength": 1},
        "subject": {"type": "string", "minLength": 1},
        "status": {"type": "string", "enum": ["open", "closed", "pending", "rejected"]},
        "evidence": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["source", "content_hash"],
                "properties": {
                    "source": {"type": "string"},
                    "content_hash": {"type": "string"},
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
        "schema_version": {"type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$"},
        "constraints": {"type": "object"}
    },
    "additionalProperties": False
}


def validate_payload(payload: Dict[str, Any], schema: Dict[str, Any]) -> None:
    """Validate a raw dict against a JSON Schema. Raises jsonschema.ValidationError on failure."""
    jsonschema.validate(instance=payload, schema=schema)
