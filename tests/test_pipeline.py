from data_loader import load_all
from decision_engine import DecisionEngine
from context_builder import ContextBuilder
from retriever import Retriever


def test_pipeline():

    data = load_all()

    builder = ContextBuilder(data)

    retriever = Retriever(
        data.sample_messages
    )

    engine = DecisionEngine()

    context = builder.build(
        data.messages[0]
    )

    retrieved = retriever.retrieve(
        context.message
    )

    decision = engine.decide(
        context,
        retrieved,
    )

    assert decision.action in (
        "notify",
        "digest",
        "mute",
    )