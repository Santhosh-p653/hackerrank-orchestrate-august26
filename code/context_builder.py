from collections import defaultdict
from dataclasses import dataclass
from typing import Any

from data_loader import DatasetBundle


@dataclass(slots=True)
class MessageContext:
    message: dict[str, Any]
    user: dict[str, Any] | None
    group: dict[str, Any] | None
    business: dict[str, Any] | None
    history: list[dict[str, Any]]
    events: list[dict[str, Any]]
    image: dict[str, Any] | None
    voice_note: dict[str, Any] | None
    notification_summary: list[dict[str, Any]]
    business_history: list[dict[str, Any]]


class ContextBuilder:

    def __init__(self, data: DatasetBundle):

        self.data = data

        self.users = {
            row["user_id"]: row
            for row in data.users
        }

        self.groups = {
            row["group_id"]: row
            for row in data.groups
        }

        self.businesses = {
            row["business_id"]: row
            for row in data.business_accounts
        }

        self.images = {
            row["image_id"]: row
            for row in data.images
        }

        self.voice_notes = {
            row["voice_note_id"]: row
            for row in data.voice_notes
        }

        self.history_by_user = defaultdict(list)
        self.events_by_user = defaultdict(list)
        self.summary_by_user = defaultdict(list)
        self.business_history_by_user = defaultdict(list)

        for row in data.message_history:
            self.history_by_user[row["user_id"]].append(row)

        for row in data.message_events:
            self.events_by_user[row["user_id"]].append(row)

        for row in data.daily_notification_summary:
            self.summary_by_user[row["user_id"]].append(row)

        for row in data.user_business_history:
            self.business_history_by_user[row["user_id"]].append(row)

    def build(self, message: dict[str, Any]) -> MessageContext:

        user_id = message["user_id"]

        media_type = message["media_type"]
        media_id = message["media_id"]

        image = None
        voice = None

        if media_type == "image":
            image = self.images.get(media_id)

        elif media_type == "voice":
            voice = self.voice_notes.get(media_id)

        return MessageContext(
            message=message,
            user=self.users.get(user_id),
            group=self.groups.get(message["group_id"]),
            business=self.businesses.get(message["business_id"]),
            history=self.history_by_user[user_id],
            events=self.events_by_user[user_id],
            image=image,
            voice_note=voice,
            notification_summary=self.summary_by_user[user_id],
            business_history=self.business_history_by_user[user_id],
        )