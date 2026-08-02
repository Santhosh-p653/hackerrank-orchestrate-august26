from dataclasses import dataclass


@dataclass(slots=True)
class AnalyzerResult:
    score: float
    reason: str
    evidence: list[str]