from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Literal
from bson import ObjectId


class SentimentRecord(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()))
    source: Literal["rss", "coingecko"]
    raw_text: str
    score: float
    label: Literal["positive", "negative", "neutral"]
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    class Config:
        populate_by_name = True