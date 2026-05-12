from fastapi import APIRouter,Depends,HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.database import get_database
from app.repositories.sentiment_repository import SentimentRepository
from app.services.sentiment_service import SentimentService
from app.models.sentiment import SentimentRecord

router =APIRouter(prefix="/sentiment",tags=["sentiment"])

def get_sentiment_service(
        db:AsyncIOMotorDatabase = Depends(get_database),
)   -> SentimentService:
    repo=SentimentRepository(db)
    return SentimentService(repository=repo)

@router.get("/latest", response_model=SentimentRecord)
async def get_latest_sentiment(
    service: SentimentService=Depends(get_sentiment_service),
):
    record = await service.get_recent(limit=1)
    if not record:
        raise HTTPException(status_code=404,detail="Sentiment Records Not Found")
    return record[0]

@router.get("/feed",response_model=list[SentimentRecord])
async def get_sentiment_feed(
    limit: int =20,
    service: SentimentService=Depends(get_sentiment_service),
):
    if limit<1 or limit>100:
        raise HTTPException(status_code=422, detail="Limit must be between 1 and 100")
    return await service.get_recent(limit=limit)

@router.get("/feed/{source}",response_model=list[SentimentRecord])
async def get_sentiment_by_source(
    source:str,
    limit:int=20,
    service: SentimentService=Depends(get_sentiment_service),
):
    if source not in ("rss","coingecko"):
        raise HTTPException(status_code=422, detail="Source not valid")
    return await service.repository.find_by_source(source=source,limit=limit)