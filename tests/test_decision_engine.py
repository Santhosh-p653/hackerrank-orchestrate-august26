from context_builder import ContextBuilder
from data_loader import load_all
from decision_engine import DecisionEngine
from retriever import Retriever


def test_decision_engine():

    data = load_all()

    builder = ContextBuilder(data)

    context = builder.build(
        data.messages[0]
    )

    retriever = Retriever(
        data.sample_messages
    )

    retrieved = retriever.retrieve(
        data.messages[0]
    )

    engine = DecisionEngine()

    decision = engine.decide(
        context,
        retrieved,
    )

    assert decision.action in {
        "notify",
        "digest",
        "mute",
    }

    assert decision.message_type is not None

    assert 0 <= decision.confidence <= 1

    assert isinstance(
        decision.evidence_message_ids,
        list,
    )