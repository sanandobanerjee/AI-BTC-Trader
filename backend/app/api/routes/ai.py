import logging
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from groq import AsyncGroq
from app.core.config import get_settings
from app.core.database import get_database
from app.repositories.sentiment_repository import SentimentRepository
from app.repositories.signal_repository import SignalRepository

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/ai", tags=["ai"])

@router.get("/explain")
async def explain_signal():
    settings = get_settings()
    client = AsyncGroq(api_key=settings.GROQ_API_KEY)
    db = get_database()
    sentiment_repo = SentimentRepository(db)
    signal_repo = SignalRepository(db)

    signal = await signal_repo.find_latest()
    records = await sentiment_repo.find_many(limit=20)

    if not signal:
        raise HTTPException(status_code=404, detail="No signal available yet. Run the pipeline first.")

    feed_summary = "\n".join([
        f"- [{r.label.upper()} {((r.score or 0) * 100):.0f}%] {r.raw_text[:120]} (source: {r.source})"
        for r in records
    ])

    prompt = f"""You are a concise crypto market analyst. Explain the following Bitcoin trading signal to a layman in plain English. Be specific — reference actual headlines and sources where relevant.

CURRENT SIGNAL: {signal.signal} (confidence: {signal.confidence * 100:.1f}%)
AVG SENTIMENT SCORE: {signal.avg_sentiment_score * 100:.1f}%
BREAKDOWN: {signal.positive_count} positive, {signal.negative_count} negative, {signal.neutral_count} neutral across {signal.sample_size} articles

RECENT HEADLINES:
{feed_summary}

Explain in under 150 words: why the signal is {signal.signal}, what headlines are driving it(mention notable positive, neutral and negative news and how they overlap each other to yield the final answer), and any notable source patterns."""

    async def stream_response():
        try:
            stream = await client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                stream=True,
                max_tokens=300,
            )
            async for chunk in stream:
                text = chunk.choices[0].delta.content
                if text:
                    yield text
        except Exception as e:
            logger.error(f"Groq stream error: {e}")
            yield "\n[Error generating analysis. Check your API key and try again.]"

    return StreamingResponse(
        stream_response(),
        media_type="text/plain",
        headers={"Access-Control-Allow-Origin": settings.FRONTEND_URL},
    )