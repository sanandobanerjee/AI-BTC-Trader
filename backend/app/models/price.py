from pydantic import BaseModel, Field
from datetime import datetime, timezone
from bson import ObjectId


class PriceSnapshot(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()))
    symbol: str = "BTC"
    price_usd: float
    market_cap_usd: float
    volume_24h_usd: float
    price_change_24h_pct: float
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    class Config:
        populate_by_name = True