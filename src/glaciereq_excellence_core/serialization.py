"""Serialization helpers for excellence pack artifacts.

All packs exchange artifacts as JSON-serialized Pydantic models.
Use serialize() / deserialize() instead of calling .model_dump() directly
so that protocol versioning metadata is always embedded.
"""
from __future__ import annotations
import json
from typing import Type, TypeVar
from pydantic import BaseModel
from .versioning import CURRENT_VERSION

T = TypeVar("T", bound=BaseModel)


def serialize(obj: BaseModel) -> str:
    """Serialize a Pydantic model to a JSON string with versioning envelope."""
    payload = {
        "_protocol_version": CURRENT_VERSION.semver,
        "_type": type(obj).__name__,
        "data": obj.model_dump(),
    }
    return json.dumps(payload, indent=2)


def deserialize(raw: str, model_cls: Type[T]) -> T:
    """Deserialize a JSON string back to a Pydantic model.
    
    Validates that the embedded protocol version is compatible before
    constructing the model so cross-pack artifacts fail fast on mismatch.
    """
    payload = json.loads(raw)
    embedded_version = payload.get("_protocol_version", "0.0.0")
    CURRENT_VERSION.assert_compatible(embedded_version)
    return model_cls(**payload["data"])
