import re
import json
from groq import AsyncGroq
from app.models.sentiment import SentimentRecord
from app.repositories.sentiment_repository import SentimentRepository
from app.core.config import get_settings

LABEL_MAP = {
    "positive": "positive",
    "negative": "negative",
    "neutral":  "neutral",
}

SENTIMENT_PROMPT = """You are a financial sentiment classifier. Classify each headline as positive, negative, or neutral from a Bitcoin/crypto investor perspective.

Return ONLY a raw JSON array. No markdown, no code fences, no explanation, no extra text before or after.
One object per headline in the same order as given.
Each object must have exactly two keys: "label" (one of: positive, negative, neutral) and "score" (float 0.0-1.0 confidence).

Example output format:
[{"label": "positive", "score": 0.92}, {"label": "neutral", "score": 0.71}]

Headlines:
{headlines}"""


class SentimentService:
    def __init__(self, repository: SentimentRepository):
        self.repository = repository
        self._settings  = get_settings()

    def _parse_response(self, raw: str, count: int) -> list[tuple[str, float]]:
        cleaned = re.sub(r"```(?:json)?", "", raw).strip().strip("`").strip()

        start = cleaned.find("[")
        end   = cleaned.rfind("]")
        if start != -1 and end != -1 and end > start:
            cleaned = cleaned[start:end + 1]

        data = json.loads(cleaned)

        results = []
        for item in data:
            label = LABEL_MAP.get(str(item.get("label", "")).lower(), "neutral")
            score = round(float(item.get("score", 0.5)), 4)
            results.append((label, score))

        if len(results) != count:
            return [("neutral", 0.5)] * count

        return results

    async def _call_api(self, texts: list[str]) -> list[tuple[str, float]]:
        client    = AsyncGroq(api_key=self._settings.GROQ_API_KEY)
        headlines = "\n".join(f"{i+1}. {t}" for i, t in enumerate(texts))
        prompt    = SENTIMENT_PROMPT.format(headlines=headlines)

        try:
            response = await client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1024,
                temperature=0.0,
            )
            raw = response.choices[0].message.content.strip()
            return self._parse_response(raw, len(texts))

        except Exception:
            return [("neutral", 0.5)] * len(texts)

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
        results      = await self._call_api([text])
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