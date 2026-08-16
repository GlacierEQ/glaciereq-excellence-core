import math
import sys
from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from glaciereq_excellence_core import (
    ApexVector,
    ApexWeights,
    FrontierSignal,
    InnovationEngineState,
    InnovationProposal,
    LanguageLane,
    ReliabilityContract,
)


def lane(lane_id: str, concern: str, language: str) -> LanguageLane:
    return LanguageLane(
        lane_id=lane_id,
        concern=concern,
        language=language,
        rationale=f"{language} owns {concern} because the boundary justifies it",
        interface="versioned schema or ABI",
        proof="repository-native tests and runtime receipt",
    )


def test_polyglot_repository_is_valid_when_each_concern_has_one_owner():
    state = InnovationEngineState(
        system_id="demo",
        lanes=[
            lane("kernel", "kernel_runtime", "Rust"),
            lane("memory", "durable_memory", "SQL"),
            lane("gpu", "accelerator_kernel", "Triton"),
            lane("control", "control_plane", "TypeScript"),
        ],
    )
    assert {item.language for item in state.lanes} == {"Rust", "SQL", "Triton", "TypeScript"}


def test_duplicate_concern_is_rejected_even_across_different_languages():
    with pytest.raises(ValueError, match="one owning lane"):
        InnovationEngineState(
            system_id="bad",
            lanes=[
                lane("memory-a", "durable_memory", "SQL"),
                lane("memory-b", "durable_memory", "Python"),
            ],
        )


def test_experiment_does_not_require_promotion_proof_but_admission_does():
    proposal = InnovationProposal(
        proposal_id="p1",
        system_id="demo",
        stage="experiment",
        baseline="current implementation",
        candidate="new implementation",
        expected_advantage="lower latency",
        experiment="bounded A/B benchmark",
        rollback="restore baseline artifact",
    )
    assert proposal.promotable() is False
    proposal.proof.append("benchmark receipt")
    assert proposal.promotable() is True


def test_reliability_requires_runtime_and_rollback_not_just_unit_tests():
    contract = ReliabilityContract(
        deterministic_tests=True,
        adversarial_tests=True,
        runtime_observation=True,
        observability=True,
        rollback_proven=True,
    )
    assert contract.operational() is True


def test_frontier_signals_are_filtered_by_release_time():
    old = FrontierSignal(
        source="vendor",
        technology="old",
        released_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        primary_source="https://example.invalid/old",
        applicability="none",
    )
    fresh = FrontierSignal(
        source="vendor",
        technology="fresh",
        released_at=datetime(2026, 8, 14, tzinfo=timezone.utc),
        primary_source="https://example.invalid/fresh",
        applicability="evaluate today",
    )
    state = InnovationEngineState(system_id="demo", frontier=[old, fresh])
    result = state.frontier_since(datetime(2026, 8, 1, tzinfo=timezone.utc))
    assert [signal.technology for signal in result] == ["fresh"]


def test_apex_prefers_stronger_coherent_system_not_the_smallest_system():
    small = ApexVector(
        capability=2,
        intelligence=2,
        reliability=3,
        efficiency=2,
        leverage=1,
        composability=2,
        reach=1,
        frontier_fitness=2,
        fragility=1,
        coordination_cost=1,
    )
    strong = ApexVector(
        capability=9,
        intelligence=9,
        reliability=9,
        efficiency=9,
        leverage=9,
        composability=9,
        reach=9,
        frontier_fitness=9,
        fragility=1,
        coordination_cost=1,
    )
    frontier = InnovationEngineState.apex_frontier([small, strong])
    assert frontier == [strong]
    assert strong.dominates(small)


def test_apex_keeps_real_tradeoffs_on_the_frontier():
    maximum_reach = ApexVector(capability=8, reach=10, reliability=7, coordination_cost=3)
    maximum_reliability = ApexVector(capability=7, reach=7, reliability=10, coordination_cost=1)
    frontier = InnovationEngineState.apex_frontier([maximum_reach, maximum_reliability])
    assert set(map(id, frontier)) == {id(maximum_reach), id(maximum_reliability)}


def test_apex_efficiency_is_a_real_dominance_dimension():
    inefficient = ApexVector(capability=8, reliability=8, efficiency=2)
    efficient = ApexVector(capability=8, reliability=8, efficiency=9)
    assert efficient.dominates(inefficient)
    assert InnovationEngineState.apex_frontier([inefficient, efficient]) == [efficient]


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_apex_rejects_non_finite_objective_values(value: float):
    with pytest.raises(ValidationError):
        ApexVector(capability=value)
    with pytest.raises(ValidationError):
        ApexWeights(capability=value)


def test_apex_rejects_finite_values_large_enough_to_overflow_weighted_math():
    with pytest.raises(ValidationError):
        ApexVector(capability=sys.float_info.max)
    with pytest.raises(ValidationError):
        ApexWeights(capability=sys.float_info.max)


def test_maximum_accepted_apex_values_keep_utility_finite():
    vector = ApexVector(
        capability=1e12,
        intelligence=1e12,
        reliability=1e12,
        efficiency=1e12,
        leverage=1e12,
        composability=1e12,
        reach=1e12,
        frontier_fitness=1e12,
        fragility=1e12,
        coordination_cost=1e12,
        unverifiability=1e12,
        duplication=1e12,
    )
    weights = ApexWeights(
        capability=1e6,
        intelligence=1e6,
        reliability=1e6,
        efficiency=1e6,
        leverage=1e6,
        composability=1e6,
        reach=1e6,
        frontier_fitness=1e6,
        fragility=1e6,
        coordination_cost=1e6,
        unverifiability=1e6,
        duplication=1e6,
    )
    assert math.isfinite(vector.utility(weights))


def test_domain_weights_order_but_do_not_delete_non_dominated_tradeoffs():
    reach_first = ApexVector(capability=7, efficiency=6, reach=10, reliability=7)
    efficiency_first = ApexVector(capability=7, efficiency=10, reach=6, reliability=7)

    reach_weights = ApexWeights(reach=5, efficiency=1)
    efficiency_weights = ApexWeights(reach=1, efficiency=5)

    reach_order = InnovationEngineState.apex_frontier(
        [reach_first, efficiency_first],
        weights=reach_weights,
    )
    efficiency_order = InnovationEngineState.apex_frontier(
        [reach_first, efficiency_first],
        weights=efficiency_weights,
    )

    assert reach_order == [reach_first, efficiency_first]
    assert efficiency_order == [efficiency_first, reach_first]
    assert set(map(id, reach_order)) == set(map(id, efficiency_order))
