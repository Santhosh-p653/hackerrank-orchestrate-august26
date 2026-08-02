from analyzers.personalization import PersonalizationAnalyzer
from context_builder import ContextBuilder
from data_loader import load_all


def test_personalization():

    data = load_all()

    builder = ContextBuilder(data)

    context = builder.build(data.messages[0])

    analyzer = PersonalizationAnalyzer()

    result = analyzer.analyze(context)

    assert 0.0 <= result.score <= 1.0
    assert isinstance(result.reason, str)