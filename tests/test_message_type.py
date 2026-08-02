from analyzers.message_type import MessageTypeAnalyzer
from context_builder import ContextBuilder
from data_loader import load_all


def test_message_type():

    data = load_all()

    builder = ContextBuilder(data)

    context = builder.build(
        data.messages[0]
    )

    analyzer = MessageTypeAnalyzer()

    result = analyzer.analyze(context)

    assert 0 <= result.score <= 1
    assert isinstance(result.reason, str)