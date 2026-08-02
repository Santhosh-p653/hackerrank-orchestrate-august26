from analyzers.safety import SafetyAnalyzer
from context_builder import ContextBuilder
from data_loader import load_all


def test_safety():

    data = load_all()

    builder = ContextBuilder(data)

    context = builder.build(
        data.messages[0]
    )

    analyzer = SafetyAnalyzer()

    result = analyzer.analyze(context)

    assert 0.0 <= result.score <= 1.0
    assert isinstance(result.reason, str)