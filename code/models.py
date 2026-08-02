from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class RetrievedExample:
    message_id: str
    action: str
    message_type: str
    reason: str
    confidence: float
    similarity: float


@dataclass(slots=True)
class Decision:
    action: str
    message_type: str
    reason: str
    confidence: float
    evidence_message_ids: list[str]


@dataclass(slots=True)
class OutputRow:
    message_id: str
    action: str
    message_type: str
    reason: str
    confidence: float
    evidence_message_ids: str


@dataclass(slots=True)
class AnalyzerContext:
    message: dict[str, Any]
    retrieved_examples: list[RetrievedExample]