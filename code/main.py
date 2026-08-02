import csv
from pathlib import Path

from data_loader import load_all
from context_builder import ContextBuilder
from retriever import Retriever
from decision_engine import DecisionEngine


OUTPUT_FILE = (
    Path(__file__).parent.parent
    / "dataset"
    / "output.csv"
)


def main():

    data = load_all()

    builder = ContextBuilder(
        data
    )

    retriever = Retriever(
        data.sample_messages
    )

    engine = DecisionEngine()

    rows = []

    for message in data.messages:

        context = builder.build(
            message
        )

        retrieved_examples = retriever.retrieve(
            message
        )

        decision = engine.decide(
            context,
            retrieved_examples,
        )

        rows.append(
            {
                "message_id": message["message_id"],
                "action": decision.action,
                "message_type": decision.message_type,
                "reason": decision.reason,
                "confidence": decision.confidence,
                "evidence_message_ids": (
                    ";".join(
                        decision.evidence_message_ids
                    )
                    if decision.evidence_message_ids
                    else "none"
                ),
            }
        )

    with OUTPUT_FILE.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "message_id",
                "action",
                "message_type",
                "reason",
                "confidence",
                "evidence_message_ids",
            ],
        )

        writer.writeheader()

        writer.writerows(
            rows
        )

    print(
        f"Generated {len(rows)} predictions at {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()