from analyzers.group import GroupAnalyzer
from context_builder import ContextBuilder
from data_loader import load_all


def test_group():

    data = load_all()

    context = ContextBuilder(data).build(
        data.messages[0]
    )

    result = GroupAnalyzer().analyze(
        context
    )

    assert 0 <= result.score <= 1