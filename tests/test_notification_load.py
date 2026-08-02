from analyzers.notification_load import NotificationLoadAnalyzer
from context_builder import ContextBuilder
from data_loader import load_all


def test_notification_load():

    data = load_all()

    builder = ContextBuilder(data)

    context = builder.build(data.messages[0])

    analyzer = NotificationLoadAnalyzer()

    result = analyzer.analyze(context)

    assert 0.0 <= result.score <= 1.0