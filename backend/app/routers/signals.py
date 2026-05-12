from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.database import get_database
from app.repositories.sentiment_repository import SentimentRepository
from app.repositories.signal_repository import SignalRepository
from app.services.signal_service import SignalService
from app.models.signal import TradingSignal
from scheduler.jobs import run_pipeline

router = APIRouter(prefix="/signals", tags=["signals"])


def get_signal_service(
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> SignalService:
    sentiment_repo = SentimentRepository(db)
    signal_repo = SignalRepository(db)
    return SignalService(
        sentiment_repository=sentiment_repo,
        signal_repository=signal_repo,
    )


@router.get("/current", response_model=TradingSignal)
async def get_current_signal(
    service: SignalService = Depends(get_signal_service),
):
    signal = await service.get_latest()
    if not signal:
        raise HTTPException(status_code=404, detail="No signal computed yet")
    return signal


@router.get("/history", response_model=list[TradingSignal])
async def get_signal_history(
    limit: int = 20,
    service: SignalService = Depends(get_signal_service),
):
    if limit < 1 or limit > 50:
        raise HTTPException(status_code=422, detail="Limit must be between 1 and 50")
    return await service.get_history(limit=limit)


@router.post("/trigger", response_model=TradingSignal)
async def trigger_pipeline(
    service: SignalService = Depends(get_signal_service),
):
    await run_pipeline()
    signal = await service.get_latest()
    if not signal:
        raise HTTPException(status_code=500, detail="Pipeline ran but produced no signal")
    return signal