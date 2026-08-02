from analyzers.base import AnalyzerResult
from context_builder import MessageContext


class MessageTypeAnalyzer:

    def analyze(
        self,
        context: MessageContext,
    ) -> AnalyzerResult:

        text = (
            context.message.get(
                "message_text",
                "",
            )
            .lower()
        )

        if any(
            word in text
            for word in [
                "otp",
                "password",
                "verify",
                "account blocked",
            ]
        ):
            return AnalyzerResult(
                score=0.95,
                reason="Possible scam content",
                evidence=[],
            )

        if any(
            word in text
            for word in [
                "pay",
                "payment",
                "invoice",
                "bill",
                "refund",
            ]
        ):
            return AnalyzerResult(
                score=0.85,
                reason="Payment related message",
                evidence=[],
            )

        if any(
            word in text
            for word in [
                "offer",
                "discount",
                "sale",
                "coupon",
            ]
        ):
            return AnalyzerResult(
                score=0.85,
                reason="Promotional content",
                evidence=[],
            )

        if any(
            word in text
            for word in [
                "happy birthday",
                "hello",
                "hi",
                "good morning",
            ]
        ):
            return AnalyzerResult(
                score=0.80,
                reason="Greeting message",
                evidence=[],
            )

        if context.message.get(
            "forwarded_count",
            0,
        ):
            return AnalyzerResult(
                score=0.70,
                reason="Forwarded message",
                evidence=[],
            )

        return AnalyzerResult(
            score=0.50,
            reason="Unable to classify",
            evidence=[],
        )