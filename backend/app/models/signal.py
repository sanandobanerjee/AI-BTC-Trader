from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Literal
from bson import ObjectId


class TradingSignal(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()))
    signal: Literal["BUY", "SELL", "HOLD"]
    confidence: float
    avg_sentiment_score: float
    positive_count: int
    negative_count: int
    neutral_count: int
    sample_size: int
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    class Config:
        populate_by_name = True