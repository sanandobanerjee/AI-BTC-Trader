import pytest
from unittest.mock import AsyncMock, patch
from app.services.sentiment_service import SentimentService


@pytest.mark.asyncio
async def test_analyse_and_store_positive():
    repo = AsyncMock()

    with patch.object(
        SentimentService,
        "_classify",
        return_value=("positive", 0.92),
    ):
        service = SentimentService(repository=repo)
        record = await service.analyse_and_store(
            text="Bitcoin is going to the moon",
            source="rss",
        )

    assert record.label == "positive"
    assert record.score == 0.92
    assert record.source == "rss"
    repo.insert.assert_called_once()


@pytest.mark.asyncio
async def test_analyse_batch_calls_insert_for_each_post():
    repo = AsyncMock()

    posts = [
        {"text": "BTC is great", "source": "rss"},
        {"text": "BTC is crashing", "source": "rss"},
        {"text": "BTC is stable", "source": "rss"},
    ]

    with patch.object(
        SentimentService,
        "_classify",
        side_effect=[
            ("positive", 0.91),
            ("negative", 0.85),
            ("neutral",  0.55),
        ],
    ):
        service = SentimentService(repository=repo)
        records = await service.analyse_batch(posts)

    assert len(records) == 3
    assert repo.insert.call_count == 3
    assert records[0].label == "positive"
    assert records[1].label == "negative"
    assert records[2].label == "neutral"