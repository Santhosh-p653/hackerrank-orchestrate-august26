class MediaProcessor:
    """
    Resolves media information from dataset files.
    """

    def __init__(self, images, voice_notes):
        self.images = images
        self.voice_notes = voice_notes

    def process(self, message):
        media_type = message.get(
            "media_type",
            "",
        )

        media_id = message.get(
            "media_id",
            "",
        )

        if not media_id:
            return {
                "has_media": False,
                "media_type": None,
                "path": None,
            }

        if media_type == "image":

            for image in self.images:

                if image.get(
                    "image_id"
                ) == media_id:

                    return {
                        "has_media": True,
                        "media_type": "image",
                        "path": image.get(
                            "file_path"
                        ),
                    }

        if media_type in [
            "audio",
            "voice",
            "voice_note",
        ]:

            for audio in self.voice_notes:

                if audio.get(
                    "voice_note_id"
                ) == media_id:

                    return {
                        "has_media": True,
                        "media_type": "audio",
                        "path": audio.get(
                            "file_path"
                        ),
                    }

        return {
            "has_media": True,
            "media_type": media_type,
            "path": None,
        }