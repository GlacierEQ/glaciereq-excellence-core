from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseModule(ABC):
    name: str = "unnamed-module"
    version: str = "0.1.0"

    @abstractmethod
    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError

    def healthcheck(self) -> Dict[str, Any]:
        return {
            "module": self.name,
            "version": self.version,
            "status": "ok",
        }
