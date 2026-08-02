from data_loader import load_all
from context_builder import ContextBuilder
from retriever import Retriever
from decision_engine import DecisionEngine
from output_generator import OutputGenerator


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
            (
                message["message_id"],
                decision,
            )
        )

    generator = OutputGenerator()

    generator.write(rows)

    print(
        f"Generated {len(rows)} predictions"
    )


if __name__ == "__main__":
    main()