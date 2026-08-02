from data_loader import load_all
from retriever import Retriever


def test_retriever():

    data = load_all()

    retriever = Retriever(
        data.sample_messages
    )

    results = retriever.retrieve(
        data.messages[0]
    )

    assert len(results) > 0

    assert results[0].similarity >= 0

    assert results[0].message_id.startswith(
        "msg_"
    )