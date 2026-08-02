import csv
from pathlib import Path

from main import main


def test_output_validation():

    main()

    output = Path("dataset/output.csv")

    assert output.exists()

    allowed_actions = {
        "notify",
        "digest",
        "mute",
    }

    required_columns = {
        "message_id",
        "action",
        "message_type",
        "reason",
        "confidence",
        "evidence_message_ids",
    }

    with output.open(
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        assert required_columns.issubset(
            reader.fieldnames
        )

        rows = list(reader)

        assert len(rows) > 0

        for row in rows:

            assert row["action"] in allowed_actions

            confidence = float(
                row["confidence"]
            )

            assert 0 <= confidence <= 1