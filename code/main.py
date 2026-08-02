from data_loader import load_all
from context_builder import ContextBuilder


def main():

    data = load_all()

    builder = ContextBuilder(data)

    print(f"Loaded {len(data.messages)} messages")

    if data.messages:

        context = builder.build(data.messages[0])

        print("First message")

        print(context.message["message_id"])

        print("User found:", context.user is not None)

        print("History:", len(context.history))

        print("Events:", len(context.events))


if __name__ == "__main__":
    main()