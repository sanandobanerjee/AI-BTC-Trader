import asyncio
import httpx
from app.models.sentiment import SentimentRecord
from app.repositories.sentiment_repository import SentimentRepository
from app.core.config import get_settings

#huggingface servers are now called instead of running FINBERT locally to drive down RAM usage. Now can be hosted on render free tier
#trade-off: higher latency on startup and rate-limiting

HF_API_URL = "https://api-inference.huggingface.co/models/ProsusAI/finbert"
LABEL_MAP = {
    "positive": "positive",
    "negative": "negative",
    "neutral":  "neutral",
}
WARMUP_RETRIES = 3
WARMUP_WAIT    = 25

class SentimentService:
    def __init__(self, repository: SentimentRepository):
        self.repository = repository
        self._settings  = get_settings()

    async def _call_api(self, texts: list[str]) -> list[tuple[str, float]]:
        headers = {"Authorization": f"Bearer {self._settings.HUGGINGFACE_API_KEY}"}
        payload = {"inputs": texts, "options": {"wait_for_model": True}}

        async with httpx.AsyncClient(timeout=60.0) as client:
            for attempt in range(WARMUP_RETRIES):
                response = await client.post(HF_API_URL, headers=headers, json=payload)
                data     = response.json()

                if isinstance(data, dict) and "loading" in data.get("error", ""):
                    wait = data.get("estimated_time", WARMUP_WAIT)
                    await asyncio.sleep(wait)
                    continue

                response.raise_for_status()

                results = []
                for item in data:
                    top   = max(item, key=lambda x: x["score"])
                    label = LABEL_MAP.get(top["label"].lower(), "neutral")
                    score = round(top["score"], 4)
                    results.append((label, score))
                return results

        return [("neutral", 0.0)] * len(texts)

    async def analyse_batch(self, posts: list[dict]) -> list[SentimentRecord]:
        texts   = [p["text"] for p in posts]
        scores  = await self._call_api(texts)
        records = []

        for post, (label, score) in zip(posts, scores):
            record = SentimentRecord(
                source=post["source"],
                raw_text=post["text"],
                score=score,
                label=label,
            )
            await self.repository.insert(record)
            records.append(record)

        return records

    async def analyse_and_store(self, text: str, source: str) -> SentimentRecord:
        results     = await self._call_api([text])
        label, score = results[0]
        record = SentimentRecord(
            source=source,
            raw_text=text,
            score=score,
            label=label,
        )
        await self.repository.insert(record)
        return record

    async def get_recent(self, limit: int = 20) -> list[SentimentRecord]:
        return await self.repository.find_many(limit=limit)