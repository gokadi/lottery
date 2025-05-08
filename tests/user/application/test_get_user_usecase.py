import uuid
from unittest.mock import Mock

import pytest

from app.user.application.get_user_by_id import GetUserByIdUseCase
from app.user.domain.entities import User


@pytest.mark.asyncio
async def test_get_user_usecase():
    repo = Mock()
    test_uuid = uuid.uuid4()
    repo.get_by_id.return_value = User(
        id=test_uuid, name="Alice", email="test@domain.com"
    )
    use_case = GetUserByIdUseCase(repo)

    result = use_case.execute(test_uuid)

    assert result.id == test_uuid
    repo.get_by_id.assert_called_once_with(test_uuid)
