import uuid
from datetime import date as date_type
from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database import Base


class LotteryModel(Base):
    __tablename__ = "lotteries"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    date: Mapped[date_type] = mapped_column(Date, nullable=False, index=True)
    winner_ballot_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )

    ballots: Mapped[List["BallotModel"]] = relationship(
        back_populates="lottery", cascade="all, delete-orphan"
    )


class BallotModel(Base):
    __tablename__ = "ballots"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False
    )
    lottery_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("lotteries.id"), nullable=False
    )
    submitted_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now(timezone.utc)
    )

    lottery: Mapped["LotteryModel"] = relationship(back_populates="ballots")
