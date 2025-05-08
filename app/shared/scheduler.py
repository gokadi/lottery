from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.lottery.application.close_lottery import CloseLotteryUseCase
from app.lottery.infrastructure.repository import SqlAlchemyLotteryRepository
from app.shared.database import SessionLocal


def start_scheduler():
    scheduler = AsyncIOScheduler()

    def job():
        session = SessionLocal()
        try:
            repo = SqlAlchemyLotteryRepository(session)
            use_case = CloseLotteryUseCase(repo, session)
            use_case.execute()
        finally:
            session.close()

    scheduler.add_job(job, CronTrigger(hour=0, minute=0))
    scheduler.start()
