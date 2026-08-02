import csv

from config import OUTPUT_FILE
from models import Decision


class OutputGenerator:

    HEADER = [
        "message_id",
        "action",
        "message_type",
        "reason",
        "confidence",
        "evidence_message_ids",
    ]

    def write(
        self,
        rows: list[tuple[str, Decision]],
    ) -> None:

        with OUTPUT_FILE.open(
            "w",
            encoding="utf-8",
            newline="",
        ) as f:

            writer = csv.writer(f)

            writer.writerow(self.HEADER)

            for message_id, decision in rows:

                writer.writerow(
                    [
                        message_id,
                        decision.action,
                        decision.message_type,
                        decision.reason,
                        f"{decision.confidence:.2f}",
                        ";".join(
                            decision.evidence_message_ids
                        )
                        if decision.evidence_message_ids
                        else "none",
                    ]
                )