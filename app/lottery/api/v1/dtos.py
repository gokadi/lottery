from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel


class BallotResponseDto(BaseModel):
    id: UUID
    user_id: UUID
    lottery_date: date
    submitted_at: datetime
