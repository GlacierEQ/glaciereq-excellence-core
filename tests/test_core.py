import json
import pytest
from glaciereq_excellence_core import (
    AuthorityMatrix,
    BaseModule,
    ClaimReceipt,
    EvidencePacket,
    EnvelopeContract,
    QuorumVote,
    serialize,
    deserialize,
    validate_payload,
    CLAIM_SCHEMA,
    ENVELOPE_SCHEMA,
    CURRENT_VERSION,
    ProtocolVersion,
)
from glaciereq_excellence_core.example_module import NullGateModule
import jsonschema


# --- Model tests ---

def test_authority_matrix_allows_expected_actions():
    matrix = AuthorityMatrix(object_type="claim", roles={"reviewer": ["read", "approve"]})
    assert matrix.allows("reviewer", "approve") is True
    assert matrix.allows("reviewer", "delete") is False


def test_quorum_vote_threshold():
    vote = QuorumVote(vote_id="q1", threshold=2, approvals=["a", "b"])
    assert vote.passed() is True


def test_quorum_vote_fails_below_threshold():
    vote = QuorumVote(vote_id="q2", threshold=3, approvals=["a"])
    assert vote.passed() is False


def test_claim_receipt_holds_evidence():
    evidence = EvidencePacket(source="unit-test", content_hash="abc123")
    receipt = ClaimReceipt(claim_id="c1", subject="demo", status="open", evidence=[evidence])
    assert receipt.evidence[0].source == "unit-test"


# --- Serialization tests ---

def test_serialize_embeds_version():
    evidence = EvidencePacket(source="test", content_hash="xyz")
    raw = serialize(evidence)
    payload = json.loads(raw)
    assert "_protocol_version" in payload
    assert payload["_protocol_version"] == CURRENT_VERSION.semver


def test_serialize_deserialize_roundtrip():
    receipt = ClaimReceipt(claim_id="c2", subject="roundtrip", status="pending")
    raw = serialize(receipt)
    recovered = deserialize(raw, ClaimReceipt)
    assert recovered.claim_id == "c2"
    assert recovered.subject == "roundtrip"


def test_deserialize_rejects_incompatible_version():
    receipt = ClaimReceipt(claim_id="c3", subject="ver", status="open")
    raw = serialize(receipt)
    payload = json.loads(raw)
    payload["_protocol_version"] = "99.0.0"
    bad_raw = json.dumps(payload)
    with pytest.raises(ValueError, match="incompatible protocol version"):
        deserialize(bad_raw, ClaimReceipt)


# --- Schema validation tests ---

def test_validate_claim_schema_passes_valid():
    validate_payload({"claim_id": "c1", "subject": "foo", "status": "open"}, CLAIM_SCHEMA)


def test_validate_claim_schema_rejects_bad_status():
    with pytest.raises(jsonschema.ValidationError):
        validate_payload({"claim_id": "c1", "subject": "foo", "status": "bogus"}, CLAIM_SCHEMA)


def test_validate_envelope_schema_passes_valid():
    validate_payload({
        "contract_id": "e1",
        "producer": "groq-batch-admission-gate",
        "consumer": "nvidia-nan-circuit-breaker",
        "schema_version": "1.0.0",
    }, ENVELOPE_SCHEMA)


# --- Versioning tests ---

def test_protocol_version_compatible_same():
    v = ProtocolVersion(1, 0, 0)
    assert v.is_compatible_with(ProtocolVersion(1, 0, 0)) is True


def test_protocol_version_incompatible_major():
    v = ProtocolVersion(1, 0, 0)
    assert v.is_compatible_with(ProtocolVersion(2, 0, 0)) is False


# --- BaseModule / Example tests ---

def test_null_gate_module_run():
    module = NullGateModule()
    result = module.run({"claim_id": "g1", "subject": "gate-test"})
    assert result["status"] == "ok"
    inner = json.loads(result["result"])
    assert inner["data"]["claim_id"] == "g1"
    assert inner["data"]["status"] == "pending"


def test_null_gate_module_healthcheck():
    module = NullGateModule()
    hc = module.healthcheck()
    assert hc["status"] == "ok"
    assert hc["module"] == "null-gate"
