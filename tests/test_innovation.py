from datetime import datetime, timezone

import pytest

from glaciereq_excellence_core import (
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
