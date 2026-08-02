from analyzers.notification_load import NotificationLoadAnalyzer
from analyzers.personalization import PersonalizationAnalyzer
from analyzers.priority import PriorityAnalyzer
from analyzers.safety import SafetyAnalyzer
from context_builder import MessageContext
from models import Decision


class DecisionEngine:
    """
    Combines analyzer outputs to determine
    notify / digest / mute.
    """

    def __init__(self):

        self.safety = SafetyAnalyzer()
        self.priority = PriorityAnalyzer()
        self.personalization = PersonalizationAnalyzer()
        self.notification_load = NotificationLoadAnalyzer()

    def decide(
        self,
        context: MessageContext,
        retrieved_examples: list[dict],
    ) -> Decision:

        safety = self.safety.analyze(context)

        priority = self.priority.analyze(context)

        personalization = self.personalization.analyze(context)

        notification = self.notification_load.analyze(context)

        # Safety first
        if safety.score >= 0.80:

            return Decision(
                action="mute",
                message_type="spam",
                reason=safety.reason,
                confidence=0.95,
                evidence_message_ids=[],
            )

        # Highly important
        if (
            priority.score >= 0.70
            and personalization.score >= 0.50
        ):

            return Decision(
                action="notify",
                message_type="urgent",
                reason=priority.reason,
                confidence=0.90,
                evidence_message_ids=[
                    row["message_id"]
                    for row in retrieved_examples
                ],
            )

        # User already overloaded
        if notification.score <= 0.40:

            return Decision(
                action="digest",
                message_type="business_update",
                reason=notification.reason,
                confidence=0.80,
                evidence_message_ids=[],
            )

        # Default behaviour
        return Decision(
            action="digest",
            message_type="unknown",
            reason="No high priority detected",
            confidence=0.65,
            evidence_message_ids=[],
        )