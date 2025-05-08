from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.lottery.api.v1.routes import router as lottery_router
from app.shared.scheduler import start_scheduler
from app.user.api.v1.routes import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(user_router, prefix="/api/v1/users")
app.include_router(lottery_router, prefix="/api/v1/lotteries")
