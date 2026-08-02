from data_loader import load_all
from context_builder import ContextBuilder


def test_context_builder():

    data = load_all()

    builder = ContextBuilder(data)

    context = builder.build(data.messages[0])

    assert context.message is not None

    assert context.user is not None