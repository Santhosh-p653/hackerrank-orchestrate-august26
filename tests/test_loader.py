from data_loader import load_all


def test_loader():
    data = load_all()

    assert len(data.messages) > 0
    assert len(data.users) > 0
    assert len(data.sample_messages) > 0