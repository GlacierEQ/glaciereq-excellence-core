from __future__ import annotations

from datetime import datetime, timezone
from typing import ClassVar, Literal

from pydantic import BaseModel, Field, FiniteFloat, model_validator


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


class ApexWeights(BaseModel):
    """Evidence-selected utility weights used only to order the Pareto frontier.

    Pareto dominance remains the primary APEX selection law. Weights never erase a
    non-dominated candidate; they provide a transparent, domain-specific ordering
    when an operator or experiment has supplied a reason to value one dimension
    more strongly than another.
    """

    capability: FiniteFloat = Field(1.0, ge=0.0)
    intelligence: FiniteFloat = Field(1.0, ge=0.0)
    reliability: FiniteFloat = Field(1.0, ge=0.0)
    efficiency: FiniteFloat = Field(1.0, ge=0.0)
    leverage: FiniteFloat = Field(1.0, ge=0.0)
    composability: FiniteFloat = Field(1.0, ge=0.0)
    reach: FiniteFloat = Field(1.0, ge=0.0)
    frontier_fitness: FiniteFloat = Field(1.0, ge=0.0)
    fragility: FiniteFloat = Field(1.0, ge=0.0)
    coordination_cost: FiniteFloat = Field(1.0, ge=0.0)
    unverifiability: FiniteFloat = Field(1.0, ge=0.0)
    duplication: FiniteFloat = Field(1.0, ge=0.0)


class ApexVector(BaseModel):
    """Machine-readable APEX objective for maximum coherent advance.

    Positive dimensions measure reachable system power. Penalty dimensions measure
    incoherence that destroys usable power. APEX does not reward smallness,
    uniformity, or immobility. It rewards the strongest non-dominated system that
    preserves truth and can prove its function.
    """

    GAIN_NAMES: ClassVar[tuple[str, ...]] = (
        "capability",
        "intelligence",
        "reliability",
        "efficiency",
        "leverage",
        "composability",
        "reach",
        "frontier_fitness",
    )
    PENALTY_NAMES: ClassVar[tuple[str, ...]] = (
        "fragility",
        "coordination_cost",
        "unverifiability",
        "duplication",
    )

    capability: FiniteFloat = Field(0.0, ge=0.0)
    intelligence: FiniteFloat = Field(0.0, ge=0.0)
    reliability: FiniteFloat = Field(0.0, ge=0.0)
    efficiency: FiniteFloat = Field(0.0, ge=0.0)
    leverage: FiniteFloat = Field(0.0, ge=0.0)
    composability: FiniteFloat = Field(0.0, ge=0.0)
    reach: FiniteFloat = Field(0.0, ge=0.0)
    frontier_fitness: FiniteFloat = Field(0.0, ge=0.0)

    fragility: FiniteFloat = Field(0.0, ge=0.0)
    coordination_cost: FiniteFloat = Field(0.0, ge=0.0)
    unverifiability: FiniteFloat = Field(0.0, ge=0.0)
    duplication: FiniteFloat = Field(0.0, ge=0.0)

    def utility(self, weights: ApexWeights | None = None) -> float:
        """Return a transparent weighted ordering score for frontier candidates."""
        selected = weights or ApexWeights()
        gains = sum(
            float(getattr(self, name)) * float(getattr(selected, name))
            for name in self.GAIN_NAMES
        )
        penalties = sum(
            float(getattr(self, name)) * float(getattr(selected, name))
            for name in self.PENALTY_NAMES
        )
        return gains - penalties

    def dominates(self, other: "ApexVector") -> bool:
        """Return true only when this vector is Pareto-superior to ``other``."""
        no_worse = all(
            getattr(self, name) >= getattr(other, name) for name in self.GAIN_NAMES
        )
        no_worse = no_worse and all(
            getattr(self, name) <= getattr(other, name) for name in self.PENALTY_NAMES
        )
        strictly_better = any(
            getattr(self, name) > getattr(other, name) for name in self.GAIN_NAMES
        ) or any(
            getattr(self, name) < getattr(other, name) for name in self.PENALTY_NAMES
        )
        return no_worse and strictly_better


class InnovationEngineState(BaseModel):
    system_id: str = Field(..., min_length=1)
    lanes: list[LanguageLane] = Field(default_factory=list)
    frontier: list[FrontierSignal] = Field(default_factory=list)
    proposals: list[InnovationProposal] = Field(default_factory=list)
    reliability: ReliabilityContract = Field(default_factory=ReliabilityContract)
    apex: ApexVector = Field(default_factory=ApexVector)

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

    @staticmethod
    def apex_frontier(
        vectors: list[ApexVector],
        weights: ApexWeights | None = None,
    ) -> list[ApexVector]:
        """Return every non-dominated candidate, ordered by declared utility."""
        frontier = [
            candidate
            for candidate in vectors
            if not any(other.dominates(candidate) for other in vectors if other is not candidate)
        ]
        return sorted(
            frontier,
            key=lambda vector: vector.utility(weights),
            reverse=True,
        )
