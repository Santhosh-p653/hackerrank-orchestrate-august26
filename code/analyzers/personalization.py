from analyzers.base import AnalyzerResult
from context_builder import MessageContext


class PersonalizationAnalyzer:
    """
    Determines how relevant a message is for this specific user.
    """

    def analyze(
        self,
        context: MessageContext,
    ) -> AnalyzerResult:

        score = 0.5
        reasons = []

        user = context.user

        if user:

            opened = int(
                user.get(
                    "messages_opened_30d",
                    0,
                )
            )

            replied = int(
                user.get(
                    "messages_replied_30d",
                    0,
                )
            )

            dismissed = int(
                user.get(
                    "notifications_dismissed_30d",
                    0,
                )
            )

            reported = int(
                user.get(
                    "messages_reported_30d",
                    0,
                )
            )

            if opened > 20:
                score += 0.15
                reasons.append(
                    "User frequently opens messages"
                )

            if replied > 5:
                score += 0.10
                reasons.append(
                    "User actively replies"
                )

            if dismissed > 20:
                score -= 0.15
                reasons.append(
                    "User often dismisses notifications"
                )

            if reported > 3:
                score -= 0.20
                reasons.append(
                    "User has reported messages before"
                )

        group = context.group

        if group:

            if str(
                group.get(
                    "group_muted_by_user",
                    "",
                )
            ).lower() == "true":

                score -= 0.20

                reasons.append(
                    "User muted this group"
                )

        business = context.business

        if business:

            if str(
                business.get(
                    "verified",
                    "",
                )
            ).lower() == "true":

                score += 0.10

                reasons.append(
                    "Verified business account"
                )

        score = max(
            0.0,
            min(
                score,
                1.0,
            ),
        )

        return AnalyzerResult(
            score=score,
            reason=(
                "; ".join(reasons)
                if reasons
                else "No strong user preference found"
            ),
            evidence=[],
        )