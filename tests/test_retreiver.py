from data_loader import load_all
from retriever import Retriever


def test_retriever():

    data = load_all()

    retriever = Retriever(data.sample_messages)

    result = retriever.retrieve(
        data.messages[0]
    )

    assert len(result) > 0

    assert "message_id" in result[0]