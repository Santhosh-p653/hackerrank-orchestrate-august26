from analyzers.notification_load import NotificationLoadAnalyzer
from analyzers.personalization import PersonalizationAnalyzer
from analyzers.priority import PriorityAnalyzer
from analyzers.safety import SafetyAnalyzer
from context_builder import MessageContext
from models import Decision


class DecisionEngine:
    """
    Combines analyzer signals into final routing decision.
    """

    def __init__(self):

        self.safety = SafetyAnalyzer()
        self.priority = PriorityAnalyzer()
        self.personalization = PersonalizationAnalyzer()
        self.notification_load = NotificationLoadAnalyzer()

    def decide(
        self,
        context: MessageContext,
        retrieved_examples: list,
    ) -> Decision:

        safety = self.safety.analyze(context)
        priority = self.priority.analyze(context)
        personalization = self.personalization.analyze(context)
        notification = self.notification_load.analyze(context)

        # Weighted scoring
        notify_score = (
            priority.score * 0.45
            + personalization.score * 0.25
            + notification.score * 0.20
            - safety.score * 0.30
        )

        mute_score = (
            safety.score * 0.70
            + (1 - personalization.score) * 0.20
        )

        digest_score = (
            1 - notify_score
        )

        evidence = [
            item.message_id
            for item in retrieved_examples[:3]
        ]

        message_type = self._infer_type(
            safety.score,
            priority.score,
            retrieved_examples,
        )

        scores = {
            "notify": notify_score,
            "digest": digest_score,
            "mute": mute_score,
        }

        action = max(
            scores,
            key=scores.get,
        )

        confidence = max(
            0.0,
            min(
                abs(scores[action]),
                1.0,
            ),
        )

        return Decision(
            action=action,
            message_type=message_type,
            reason=self._reason(
                action,
                safety.reason,
                priority.reason,
                personalization.reason,
            ),
            confidence=round(
                confidence,
                2,
            ),
            evidence_message_ids=evidence,
        )

    def _infer_type(
        self,
        safety_score,
        priority_score,
        retrieved_examples,
    ):

        if safety_score >= 0.7:
            return "scam"

        if priority_score >= 0.7:
            return "urgent"

        if retrieved_examples:
            return retrieved_examples[0].message_type

        return "unknown"

    def _reason(
        self,
        action,
        safety,
        priority,
        personalization,
    ):

        return (
            f"Decision={action}. "
            f"Safety: {safety}. "
            f"Priority: {priority}. "
            f"User profile: {personalization}"
        )