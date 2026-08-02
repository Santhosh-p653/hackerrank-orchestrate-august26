from models import RetrievedExample, Decision, OutputRow


def test_models():

    example = RetrievedExample(
        message_id="msg_001",
        action="notify",
        message_type="urgent",
        reason="Emergency",
        confidence=0.95,
        similarity=0.90,
    )

    decision = Decision(
        action="notify",
        message_type="urgent",
        reason="Emergency",
        confidence=0.95,
        evidence_message_ids=["msg_001"],
    )

    output = OutputRow(
        message_id="msg_100",
        action="notify",
        message_type="urgent",
        reason="Emergency",
        confidence=0.95,
        evidence_message_ids="msg_001",
    )

    assert example.message_id == "msg_001"
    assert decision.action == "notify"
    assert output.message_id == "msg_100"