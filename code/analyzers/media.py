from analyzers.base import AnalyzerResult
from context_builder import MessageContext


class MediaAnalyzer:
    """
    Evaluates media attached to messages.
    """

    def analyze(
        self,
        context: MessageContext,
    ) -> AnalyzerResult:

        media = getattr(
            context,
            "media",
            None,
        )

        if not media or not media.get(
            "has_media"
        ):

            return AnalyzerResult(
                score=0.5,
                reason="No media attached",
                evidence=[],
            )

        media_type = media.get(
            "media_type",
            "",
        )

        if media_type == "image":

            return AnalyzerResult(
                score=0.7,
                reason="Image attachment available for analysis",
                evidence=[],
            )

        if media_type == "audio":

            return AnalyzerResult(
                score=0.7,
                reason="Voice message available for transcription",
                evidence=[],
            )

        return AnalyzerResult(
            score=0.5,
            reason="Unknown media attachment",
            evidence=[],
        )