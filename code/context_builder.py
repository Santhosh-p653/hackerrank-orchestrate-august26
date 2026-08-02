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

    def build(self, message: dict[str, Any]) -> MessageContext:

        user_id = message["user_id"]
        group_id = message["group_id"]
        business_id = message["business_id"]
        media_type = message["media_type"]
        media_id = message["media_id"]

        history = [
            row
            for row in self.data.message_history
            if row["user_id"] == user_id
        ]

        events = [
            row
            for row in self.data.message_events
            if row["user_id"] == user_id
        ]

        notification_summary = [
            row
            for row in self.data.daily_notification_summary
            if row["user_id"] == user_id
        ]

        business_history = [
            row
            for row in self.data.user_business_history
            if row["user_id"] == user_id
        ]

        image = None
        voice = None

        if media_type == "image":
            image = self.images.get(media_id)

        elif media_type == "voice":
            voice = self.voice_notes.get(media_id)

        return MessageContext(
            message=message,
            user=self.users.get(user_id),
            group=self.groups.get(group_id),
            business=self.businesses.get(business_id),
            history=history,
            events=events,
            image=image,
            voice_note=voice,
            notification_summary=notification_summary,
            business_history=business_history,
        )