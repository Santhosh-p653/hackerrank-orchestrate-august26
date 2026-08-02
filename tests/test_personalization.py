from context_builder import ContextBuilder
from data_loader import load_all
from analyzers.personalization import PersonalizationAnalyzer


def test_personalization():

    data = load_all()

    builder = ContextBuilder(data)

    context = builder.build(
        data.messages[0]
    )

    analyzer = PersonalizationAnalyzer()

    result = analyzer.analyze(
        context
    )

    assert 0 <= result.score <= 1

    assert isinstance(
        result.reason,
        str,
    )