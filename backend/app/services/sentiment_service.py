import re
import json
import logging
from groq import AsyncGroq
from app.models.sentiment import SentimentRecord
from app.repositories.sentiment_repository import SentimentRepository
from app.core.config import get_settings

logger = logging.getLogger(__name__)

LABEL_MAP = {
    "positive": "positive",
    "negative": "negative",
    "neutral":  "neutral",
}

SENTIMENT_INSTRUCTIONS = (
    "You are a financial sentiment classifier. Classify each headline as "
    "positive, negative, or neutral from a Bitcoin/crypto investor perspective.\n\n"
    "Return ONLY a raw JSON array. No markdown, no code fences, no explanation, "
    "no extra text before or after.\n"
    "One object per headline in the same order as given.\n"
    'Each object must have exactly two keys: "label" (one of: positive, negative, neutral) '
    'and "score" (float 0.0-1.0 confidence).\n\n'
    "Be decisive. Most financial headlines lean positive or negative rather than "
    "perfectly neutral — reserve neutral only for headlines with no clear market implication.\n\n"
    'Example output format:\n'
    '[{"label": "positive", "score": 0.92}, {"label": "neutral", "score": 0.71}]\n\n'
    "Headlines:\n"
)

OBJECT_PATTERN = re.compile(
    r'\{\s*"label"\s*:\s*"(\w+)"\s*,\s*"score"\s*:\s*([\d.]+)\s*\}'
)


class SentimentService:
    def __init__(self, repository: SentimentRepository):
        self.repository = repository
        self._settings  = get_settings()

    def _parse_response(self, raw: str, count: int) -> list[tuple[str, float]]:
        cleaned = re.sub(r"```(?:json)?", "", raw).strip().strip("`").strip()

        try:
            start = cleaned.find("[")
            end   = cleaned.rfind("]")
            if start != -1 and end != -1 and end > start:
                candidate = cleaned[start:end + 1]
                data = json.loads(candidate)

                results = []
                for item in data:
                    label = LABEL_MAP.get(str(item.get("label", "")).lower(), "neutral")
                    score = round(float(item.get("score", 0.5)), 4)
                    results.append((label, score))

                if len(results) == count:
                    return results

                logger.warning(f"Full-array parse gave {len(results)} items, expected {count}. Falling back to regex extraction.")

        except (json.JSONDecodeError, ValueError, TypeError) as e:
            logger.warning(f"Full-array JSON parse failed ({e}). Falling back to regex extraction.")

        matches = OBJECT_PATTERN.findall(cleaned)
        if matches:
            results = []
            for label_raw, score_raw in matches:
                label = LABEL_MAP.get(label_raw.lower(), "neutral")
                score = round(float(score_raw), 4)
                results.append((label, score))

            if len(results) == count:
                return results

            logger.warning(f"Regex extraction gave {len(results)} items, expected {count}. Padding/truncating.")
            if len(results) > count:
                return results[:count]
            return results + [("neutral", 0.5)] * (count - len(results))

        logger.error("Both full-array and regex parsing failed. Returning neutral fallback for entire batch.")
        return [("neutral", 0.5)] * count

    async def _call_api(self, texts: list[str]) -> list[tuple[str, float]]:
        client    = AsyncGroq(api_key=self._settings.GROQ_API_KEY)
        headlines = "\n".join(f"{i+1}. {t}" for i, t in enumerate(texts))
        prompt    = SENTIMENT_INSTRUCTIONS + headlines

        try:
            response = await client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2048,
                temperature=0.3,
            )
            raw = response.choices[0].message.content.strip()
            logger.info(f"Groq raw response ({len(raw)} chars): {raw[:800]}")
            return self._parse_response(raw, len(texts))

        except Exception as e:
            logger.error(f"Groq sentiment call failed: {e}")
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
                url=post.get("url"),
            )
            await self.repository.insert(record)
            records.append(record)

        return records

    async def analyse_and_store(self, text: str, source: str, url: str | None = None) -> SentimentRecord:
        results      = await self._call_api([text])
        label, score = results[0]
        record = SentimentRecord(
            source=source,
            raw_text=text,
            score=score,
            label=label,
            url=url,
        )
        await self.repository.insert(record)
        return record

    async def get_recent(self, limit: int = 20) -> list[SentimentRecord]:
        return await self.repository.find_many(limit=limit)