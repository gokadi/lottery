import uuid

from app.user.domain.entities import User


def test_user_creation():
    user = User(id=uuid.uuid4(), name="Alice", email="test@domain.com")

    assert user.name == "Alice"
