"""Protocol versioning for cross-pack artifact exchange.

Every serialized artifact embeds the protocol version it was produced under.
Receivers call ProtocolVersion.assert_compatible() to reject stale or
future artifacts before attempting deserialization.
"""
from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class ProtocolVersion:
    major: int
    minor: int
    patch: int

    @property
    def semver(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    @classmethod
    def parse(cls, semver: str) -> "ProtocolVersion":
        parts = semver.split(".")
        if len(parts) != 3:
            raise ValueError(f"Invalid semver string: {semver!r}")
        return cls(major=int(parts[0]), minor=int(parts[1]), patch=int(parts[2]))

    def is_compatible_with(self, other: "ProtocolVersion") -> bool:
        """Compatible when major versions match and other.minor <= self.minor."""
        return self.major == other.major and other.minor <= self.minor

    def assert_compatible(self, semver_str: str) -> None:
        other = ProtocolVersion.parse(semver_str)
        if not self.is_compatible_with(other):
            raise ValueError(
                f"Protocol version mismatch: current={self.semver}, artifact={semver_str}. "
                "Artifact was produced by an incompatible protocol version."
            )


# Bump this on every breaking change to the shared contract.
CURRENT_VERSION = ProtocolVersion(major=1, minor=0, patch=0)
