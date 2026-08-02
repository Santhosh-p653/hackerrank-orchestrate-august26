from analyzers.base import AnalyzerResult
from context_builder import MessageContext


class MediaAnalyzer:
    """
    Evaluates image and voice attachments.
    """

    def analyze(
        self,
        context: MessageContext,
    ) -> AnalyzerResult:

        if context.image:

            return AnalyzerResult(
                score=0.7,
                reason="Image attachment available for analysis",
                evidence=[],
            )

        if context.voice_note:

            return AnalyzerResult(
                score=0.7,
                reason="Voice message available for transcription",
                evidence=[],
            )

        return AnalyzerResult(
            score=0.5,
            reason="No media attachment",
            evidence=[],
        )