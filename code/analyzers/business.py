from analyzers.base import AnalyzerResult
from context_builder import MessageContext


class BusinessAnalyzer:
    """
    Evaluates trust and relevance of business messages.
    """

    def analyze(
        self,
        context: MessageContext,
    ) -> AnalyzerResult:

        score = 0.5
        reasons = []

        business = context.business

        if not business:
            return AnalyzerResult(
                score=score,
                reason="No business context",
                evidence=[],
            )

        verified = str(
            business.get("verified", "")
        ).lower()

        if verified == "true":
            score += 0.2
            reasons.append(
                "Verified business account"
            )

        reports = int(
            business.get(
                "user_reports_30d",
                0,
            )
        )

        if reports > 5:
            score -= 0.3
            reasons.append(
                "Business has user reports"
            )

        age = int(
            business.get(
                "account_age_days",
                0,
            )
        )

        if age > 180:
            score += 0.1
            reasons.append(
                "Established business account"
            )

        history = context.business_history

        if history and isinstance(history, list):

            # use latest relationship record
            record = history[0]

            opted_out = record.get(
                "promotions_opted_out_at",
                "",
            )

            if opted_out:
                score -= 0.2
                reasons.append(
                    "User opted out of promotions"
                )

            activity = int(
                record.get(
                    "activity_count_180d",
                    0,
                )
            )

            if activity > 10:
                score += 0.1
                reasons.append(
                    "User has business relationship"
                )

        score = max(
            0.0,
            min(score, 1.0),
        )

        return AnalyzerResult(
            score=score,
            reason=(
                "; ".join(reasons)
                if reasons
                else "No business signals"
            ),
            evidence=[],
        )