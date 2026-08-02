from data_loader import load_all


def main():
    data = load_all()

    print("Datasets loaded successfully.\n")

    print(f"Messages            : {len(data.messages)}")
    print(f"Users               : {len(data.users)}")
    print(f"Groups              : {len(data.groups)}")
    print(f"Group Members       : {len(data.group_members)}")
    print(f"Businesses          : {len(data.business_accounts)}")
    print(f"History             : {len(data.message_history)}")
    print(f"Events              : {len(data.message_events)}")
    print(f"Images              : {len(data.images)}")
    print(f"Voice Notes         : {len(data.voice_notes)}")
    print(f"Sample Messages     : {len(data.sample_messages)}")


if __name__ == "__main__":
    main()