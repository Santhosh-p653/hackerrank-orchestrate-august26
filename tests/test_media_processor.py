from data_loader import load_all
from media import MediaProcessor


def test_media_processor():

    data = load_all()

    processor = MediaProcessor(
        data.images,
        data.voice_notes,
    )

    result = processor.process(
        data.messages[0]
    )

    assert "has_media" in result

    assert "media_type" in result