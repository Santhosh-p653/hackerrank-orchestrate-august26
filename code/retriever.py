from rapidfuzz import fuzz

from models import RetrievedExample


class Retriever:
    """
    Retrieves similar labelled examples from sample_messages.csv.
    """

    def __init__(self, sample_messages: list[dict]):
        self.sample_messages = sample_messages

    def retrieve(
        self,
        message: dict,
        top_k: int = 3,
    ) -> list[RetrievedExample]:

        current_text = (
            message.get("message_text", "")
            .lower()
            .strip()
        )

        conversation_type = message.get(
            "conversation_type",
            "",
        )

        media_type = message.get(
            "media_type",
            "",
        )

        scored = []

        for sample in self.sample_messages:

            score = fuzz.token_sort_ratio(
                current_text,
                sample.get(
                    "message_text",
                    "",
                ).lower(),
            )

            if (
                sample.get("conversation_type")
                == conversation_type
            ):
                score += 5

            if (
                sample.get("media_type")
                == media_type
            ):
                score += 5

            scored.append(
                (
                    score,
                    sample,
                )
            )

        scored.sort(
            reverse=True,
            key=lambda x: x[0],
        )

        results = []

        for score, sample in scored[:top_k]:

            results.append(
                RetrievedExample(
                    message_id=sample["message_id"],
                    action=sample["action"],
                    message_type=sample["message_type"],
                    reason=sample["reason"],
                    confidence=float(
                        sample["confidence"]
                    ),
                    similarity=score / 100.0,
                )
            )

        return results