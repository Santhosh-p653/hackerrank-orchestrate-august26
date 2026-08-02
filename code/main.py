from context_builder import ContextBuilder
from data_loader import load_all
from decision_engine import DecisionEngine
from output_generator import OutputGenerator
from retriever import Retriever


def main():

    print("Loading datasets...")

    data = load_all()

    builder = ContextBuilder(data)

    retriever = Retriever(data.sample_messages)

    engine = DecisionEngine()

    generator = OutputGenerator()

    rows = []

    total = len(data.messages)

    for index, message in enumerate(data.messages, start=1):

        context = builder.build(message)

        retrieved = retriever.retrieve(
            context.message
        )

        decision = engine.decide(
            context,
            retrieved,
        )

        rows.append(
            (
                message["message_id"],
                decision,
            )
        )

        if index % 25 == 0 or index == total:
            print(f"Processed {index}/{total}")

    generator.write(rows)

    print("Finished.")
    print("output.csv generated successfully.")


if __name__ == "__main__":
    main()