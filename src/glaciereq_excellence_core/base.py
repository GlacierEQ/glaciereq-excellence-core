"""Abstract base class for all excellence pack modules.

Every downstream excellence pack must subclass BaseModule and implement run().
The contract guarantees that:
  - run() accepts a typed dict payload and returns a typed dict result.
  - healthcheck() always returns a status report without side effects.
  - The module declares its own name and version as class attributes.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseModule(ABC):
    name: str = "unnamed-module"
    version: str = "0.1.0"

    @abstractmethod
    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the module's primary logic against a payload dict.
        
        Args:
            payload: Arbitrary input data. Validate with validate_payload() before use.
        Returns:
            A dict containing at minimum: {"status": str, "result": Any}
        """
        raise NotImplementedError

    def healthcheck(self) -> Dict[str, Any]:
        """Return a no-side-effect status report for orchestration polling."""
        return {
            "module": self.name,
            "version": self.version,
            "status": "ok",
        }
