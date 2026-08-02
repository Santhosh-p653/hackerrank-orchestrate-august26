from difflib import SequenceMatcher


class Retriever:
    def __init__(self, sample_messages: list[dict]):
        self.sample_messages = sample_messages

    @staticmethod
    def _similarity(a: str, b: str) -> float:
        return SequenceMatcher(
            None,
            (a or "").lower(),
            (b or "").lower(),
        ).ratio()

    def retrieve(
        self,
        message: dict,
        top_k: int = 3,
    ) -> list[dict]:

        text = message.get("message_text", "")

        scored = []

        for sample in self.sample_messages:

            score = self._similarity(
                text,
                sample.get("message_text", ""),
            )

            scored.append((score, sample))

        scored.sort(
            key=lambda x: x[0],
            reverse=True,
        )

        return [
            sample
            for score, sample in scored[:top_k]
        ]