import pytest
from unittest.mock import AsyncMock
from app.services.signal_service import SignalService
from app.models.sentiment import SentimentRecord
from datetime import datetime


def make_record(label: str, score: float) -> SentimentRecord:
    return SentimentRecord(
        source="rss",
        raw_text="test",
        score=score,
        label=label,
        created_at=datetime.now(),
    )


@pytest.mark.asyncio
async def test_buy_signal_when_mostly_positive():
    sentiment_repo = AsyncMock()
    signal_repo = AsyncMock()

    sentiment_repo.find_many.return_value = [
        make_record("positive", 0.9),
        make_record("positive", 0.85),
        make_record("positive", 0.88),
        make_record("positive", 0.91),
        make_record("positive", 0.87),
        make_record("negative", 0.7),
        make_record("neutral",  0.5),
    ]

    service = SignalService(
        sentiment_repository=sentiment_repo,
        signal_repository=signal_repo,
    )

    signal = await service.compute_and_store(sample_size=7)

    assert signal.signal == "BUY"
    assert signal.positive_count == 5
    assert signal.confidence > 0


@pytest.mark.asyncio
async def test_hold_signal_when_insufficient_data():
    sentiment_repo = AsyncMock()
    signal_repo = AsyncMock()

    sentiment_repo.find_many.return_value = [
        make_record("positive", 0.9),
        make_record("negative", 0.8),
    ]

    service = SignalService(
        sentiment_repository=sentiment_repo,
        signal_repository=signal_repo,
    )

    signal = await service.compute_and_store(sample_size=2)

    assert signal.signal == "HOLD"
    assert signal.confidence == 0.0