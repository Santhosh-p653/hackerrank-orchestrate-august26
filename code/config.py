from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = ROOT_DIR / "dataset"
MEDIA_DIR = DATASET_DIR / "media"


CSV_FILES = {
    "messages": DATASET_DIR / "messages.csv",
    "users": DATASET_DIR / "users.csv",
    "groups": DATASET_DIR / "groups.csv",
    "group_members": DATASET_DIR / "group_members.csv",
    "business_accounts": DATASET_DIR / "business_accounts.csv",
    "user_business_history": DATASET_DIR / "user_business_history.csv",
    "message_history": DATASET_DIR / "message_history.csv",
    "message_events": DATASET_DIR / "message_events.csv",
    "images": DATASET_DIR / "images.csv",
    "voice_notes": DATASET_DIR / "voice_notes.csv",
    "daily_notification_summary": DATASET_DIR / "daily_notification_summary.csv",
    "sample_messages": DATASET_DIR / "sample_messages.csv",
}


OUTPUT_FILE = DATASET_DIR / "output.csv"