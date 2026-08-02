from analyzers.notification_load import NotificationLoadAnalyzer
from analyzers.personalization import PersonalizationAnalyzer
from analyzers.priority import PriorityAnalyzer
from analyzers.safety import SafetyAnalyzer
from analyzers.message_type import MessageTypeAnalyzer
from analyzers.business import BusinessAnalyzer
from analyzers.group import GroupAnalyzer
from analyzers.media import MediaAnalyzer

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
        self.message_type = MessageTypeAnalyzer()
        self.business = BusinessAnalyzer()
        self.group = GroupAnalyzer()
        self.media = MediaAnalyzer()

    def decide(
        self,
        context: MessageContext,
        retrieved_examples: list,
    ) -> Decision:

        safety = self.safety.analyze(context)
        priority = self.priority.analyze(context)
        personalization = self.personalization.analyze(context)
        notification = self.notification_load.analyze(context)
        message_type_result = self.message_type.analyze(context)

        business = self.business.analyze(context)
        group = self.group.analyze(context)
        media = self.media.analyze(context)

        notify_score = (
            priority.score * 0.30
            + personalization.score * 0.20
            + group.score * 0.15
            + business.score * 0.15
            + notification.score * 0.10
            + media.score * 0.10
            - safety.score * 0.15
        )

        mute_score = (
            safety.score * 0.65
            + (1 - personalization.score) * 0.20
            + (1 - business.score) * 0.15
        )

        digest_score = (
            (1 - priority.score) * 0.40
            + notification.score * 0.40
            + (1 - personalization.score) * 0.20
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

        evidence = self._select_evidence(
            retrieved_examples,
            action,
        )

        message_type = self._map_message_type(
            message_type_result.reason
        )

        sorted_scores = sorted(
            scores.values(),
            reverse=True,
        )

        confidence = max(
            0.0,
            min(
                sorted_scores[0] - sorted_scores[1],
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

    def _select_evidence(
        self,
        retrieved_examples,
        action,
    ):

        matched = [
            item
            for item in retrieved_examples
            if item.action == action
        ]

        if not matched:
            matched = retrieved_examples

        matched.sort(
            key=lambda x: x.similarity,
            reverse=True,
        )

        return [
            item.message_id
            for item in matched[:3]
        ]

    def _map_message_type(
        self,
        reason,
    ):

        reason = reason.lower()

        if "scam" in reason:
            return "scam"

        if "payment" in reason:
            return "payment"

        if "promotion" in reason:
            return "promotion"

        if "greeting" in reason:
            return "greeting"

        if "forward" in reason:
            return "forward"

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