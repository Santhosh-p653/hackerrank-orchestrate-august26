from dataclasses import dataclass
from config import CSV_FILES
from utils import load_csv


@dataclass
class DatasetBundle:
    messages: list
    users: list
    groups: list
    group_members: list
    business_accounts: list
    user_business_history: list
    message_history: list
    message_events: list
    images: list
    voice_notes: list
    daily_notification_summary: list
    sample_messages: list


def load_all() -> DatasetBundle:
    return DatasetBundle(
        messages=load_csv(CSV_FILES["messages"]),
        users=load_csv(CSV_FILES["users"]),
        groups=load_csv(CSV_FILES["groups"]),
        group_members=load_csv(CSV_FILES["group_members"]),
        business_accounts=load_csv(CSV_FILES["business_accounts"]),
        user_business_history=load_csv(CSV_FILES["user_business_history"]),
        message_history=load_csv(CSV_FILES["message_history"]),
        message_events=load_csv(CSV_FILES["message_events"]),
        images=load_csv(CSV_FILES["images"]),
        voice_notes=load_csv(CSV_FILES["voice_notes"]),
        daily_notification_summary=load_csv(
            CSV_FILES["daily_notification_summary"]
        ),
        sample_messages=load_csv(CSV_FILES["sample_messages"]),
    )