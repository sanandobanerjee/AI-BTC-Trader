from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.database import get_database
from app.models.price import PriceSnapshot

router = APIRouter(prefix="/price", tags=["price"])


def get_price_collection(
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    return db["prices"]


def doc_to_snapshot(doc: dict) -> PriceSnapshot:
    if "_id" in doc:
        doc["id"] = str(doc.pop("_id"))
    return PriceSnapshot(**doc)


@router.get("/btc", response_model=PriceSnapshot)
async def get_btc_price(
    collection=Depends(get_price_collection),
):
    doc = await collection.find_one(
        filter={},
        sort=[("created_at", -1)]
    )
    if doc is None:
        raise HTTPException(
            status_code=404,
            detail="No price data available yet"
        )
    return doc_to_snapshot(doc)


@router.get("/btc/history", response_model=list[PriceSnapshot])
async def get_btc_price_history(
    limit: int = 24,
    collection=Depends(get_price_collection),
):
    if limit < 1 or limit > 288:
        raise HTTPException(
            status_code=422,
            detail="Limit must be between 1 and 288"
        )
    cursor = collection.find({}).sort("created_at", -1).limit(limit)
    docs = await cursor.to_list(length=limit)
    return [doc_to_snapshot(doc) for doc in docs]