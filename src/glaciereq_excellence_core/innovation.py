from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, Field, model_validator


Stage = Literal["observe", "experiment", "admit", "retire"]


class LanguageLane(BaseModel):
    lane_id: str = Field(..., min_length=1)
    concern: str = Field(..., min_length=1)
    language: str = Field(..., min_length=1)
    rationale: str = Field(..., min_length=1)
    interface: str = Field(..., min_length=1)
    proof: str = Field(..., min_length=1)


class FrontierSignal(BaseModel):
    source: str = Field(..., min_length=1)
    technology: str = Field(..., min_length=1)
    released_at: datetime
    observed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    primary_source: str = Field(..., min_length=1)
    applicability: str = Field(..., min_length=1)


class InnovationProposal(BaseModel):
    proposal_id: str = Field(..., min_length=1)
    system_id: str = Field(..., min_length=1)
    stage: Stage = "observe"
    baseline: str = Field(..., min_length=1)
    candidate: str = Field(..., min_length=1)
    expected_advantage: str = Field(..., min_length=1)
    experiment: str = Field(..., min_length=1)
    proof: list[str] = Field(default_factory=list)
    rollback: str = Field(..., min_length=1)

    def promotable(self) -> bool:
        return self.stage in {"experiment", "admit"} and bool(self.proof)


class ReliabilityContract(BaseModel):
    deterministic_tests: bool = False
    adversarial_tests: bool = False
    runtime_observation: bool = False
    observability: bool = False
    rollback_proven: bool = False

    def operational(self) -> bool:
        return all(self.model_dump().values())


class InnovationEngineState(BaseModel):
    system_id: str = Field(..., min_length=1)
    lanes: list[LanguageLane] = Field(default_factory=list)
    frontier: list[FrontierSignal] = Field(default_factory=list)
    proposals: list[InnovationProposal] = Field(default_factory=list)
    reliability: ReliabilityContract = Field(default_factory=ReliabilityContract)

    @model_validator(mode="after")
    def lanes_are_owned_once(self) -> "InnovationEngineState":
        ids = [lane.lane_id for lane in self.lanes]
        concerns = [lane.concern for lane in self.lanes]
        if len(ids) != len(set(ids)):
            raise ValueError("language lane_id ownership must be unique")
        if len(concerns) != len(set(concerns)):
            raise ValueError("each architecture concern must have one owning lane")
        return self

    def frontier_since(self, since: datetime) -> list[FrontierSignal]:
        return sorted(
            [signal for signal in self.frontier if signal.released_at >= since],
            key=lambda signal: signal.released_at,
            reverse=True,
        )
