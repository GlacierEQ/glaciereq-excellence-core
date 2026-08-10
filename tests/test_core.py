from glaciereq_excellence_core import AuthorityMatrix, BaseModule, EvidencePacket, ClaimReceipt, QuorumVote


class DemoModule(BaseModule):
    name = "demo-module"

    def run(self, payload):
        return {"received": payload, "status": "processed"}


def test_authority_matrix_allows_expected_actions():
    matrix = AuthorityMatrix(object_type="claim", roles={"reviewer": ["read", "approve"]})
    assert matrix.allows("reviewer", "approve") is True
    assert matrix.allows("reviewer", "delete") is False


def test_quorum_vote_threshold():
    vote = QuorumVote(vote_id="q1", threshold=2, approvals=["a", "b"])
    assert vote.passed() is True


def test_claim_receipt_holds_evidence():
    evidence = EvidencePacket(source="unit-test", content_hash="abc123")
    receipt = ClaimReceipt(claim_id="c1", subject="demo", status="open", evidence=[evidence])
    assert receipt.evidence[0].source == "unit-test"


def test_base_module_healthcheck():
    module = DemoModule()
    assert module.healthcheck()["status"] == "ok"
