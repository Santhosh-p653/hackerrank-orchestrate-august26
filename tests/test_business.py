from analyzers.business import BusinessAnalyzer
from context_builder import ContextBuilder
from data_loader import load_all


def test_business():

    data = load_all()

    context = ContextBuilder(data).build(
        data.messages[0]
    )

    result = BusinessAnalyzer().analyze(
        context
    )

    assert 0 <= result.score <= 1