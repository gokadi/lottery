from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class UserResponseDto(BaseModel):
    id: UUID
    email: str
    name: Optional[str] = None
    banned_at: Optional[datetime] = None
