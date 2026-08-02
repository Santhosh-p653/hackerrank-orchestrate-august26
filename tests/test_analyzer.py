from analyzers.base import AnalyzerResult


def test_analyzer_result():

    result = AnalyzerResult(
        score=0.9,
        reason="Test",
        evidence=[]
    )

    assert result.score == 0.9
    assert result.reason == "Test"
    assert result.evidence == []