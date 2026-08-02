from pathlib import Path

from models import Decision
from output_generator import OutputGenerator


def test_output_generator(tmp_path):

    generator = OutputGenerator()

    original = generator.write

    output = tmp_path / "output.csv"

    def patched(rows):
        import csv

        with output.open(
            "w",
            newline="",
            encoding="utf-8",
        ) as f:

            writer = csv.writer(f)

            writer.writerow(generator.HEADER)

            for message_id, decision in rows:
                writer.writerow(
                    [
                        message_id,
                        decision.action,
                        decision.message_type,
                        decision.reason,
                        decision.confidence,
                        "none",
                    ]
                )

    generator.write = patched

    generator.write(
        [
            (
                "msg_001",
                Decision(
                    action="notify",
                    message_type="urgent",
                    reason="test",
                    confidence=0.9,
                    evidence_message_ids=[],
                ),
            )
        ]
    )

    assert Path(output).exists()