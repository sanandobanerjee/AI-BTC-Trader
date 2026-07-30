import re
import asyncio
import time
import httpx
import feedparser
from app.core.config import get_settings

settings = get_settings()

RSS_FEEDS = [
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "https://cointelegraph.com/rss",
    "https://decrypt.co/feed",
    "https://bitcoinmagazine.com/.rss/full/",
    "https://cryptoslate.com/feed/",
]

PRICE_RETRIES      = 2
PRICE_RETRY_WAIT   = 20
CACHE_TTL_SECONDS  = 90

HTML_TAG_PATTERN = re.compile(r"<[^>]*>")


class RSSNewsClient:

    def _clean_text(self, raw: str) -> str:
        no_tags = HTML_TAG_PATTERN.sub(" ", raw)
        return re.sub(r"\s+", " ", no_tags).strip()

    def get_btc_posts(self, limit: int = 25) -> list[dict]:
        results  = []
        per_feed = max(1, limit // len(RSS_FEEDS))

        for feed_url in RSS_FEEDS:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:per_feed]:
                    title   = self._clean_text(entry.get("title", ""))
                    summary = self._clean_text(entry.get("summary", ""))
                    link    = entry.get("link", "").strip()
                    if not title:
                        continue
                    text = f"{title}. {summary[:150]}".strip()
                    results.append({"text": text, "source": "rss", "url": link})
            except Exception:
                continue

        return results[:limit]


class IngestionService:

    def __init__(self):
        self.rss_client   = RSSNewsClient()
        self._price_cache: dict | None = None
        self._cache_time:  float = 0.0

    async def fetch_news(self, limit: int = 25) -> list[dict]:
        loop  = asyncio.get_event_loop()
        posts = await loop.run_in_executor(
            None,
            lambda: self.rss_client.get_btc_posts(limit=limit),
        )
        return posts

    def _cache_is_fresh(self) -> bool:
        return (
            self._price_cache is not None
            and (time.monotonic() - self._cache_time) < CACHE_TTL_SECONDS
        )

    async def fetch_price(self) -> dict:
        if self._cache_is_fresh():
            return self._price_cache

        url    = f"{settings.COINGECKO_BASE_URL}/simple/price"
        params = {
            "ids":               "bitcoin",
            "vs_currencies":     "usd",
            "include_market_cap": "true",
            "include_24hr_vol":  "true",
            "include_24hr_change": "true",
        }

        async with httpx.AsyncClient(timeout=15.0) as client:
            for attempt in range(PRICE_RETRIES):
                response = await client.get(url, params=params)

                if response.status_code == 429:
                    if self._price_cache is not None:
                        return self._price_cache
                    await asyncio.sleep(PRICE_RETRY_WAIT * (attempt + 1))
                    continue

                response.raise_for_status()
                bitcoin = response.json()["bitcoin"]
                result  = {
                    "price_usd":            bitcoin["usd"],
                    "market_cap_usd":       bitcoin["usd_market_cap"],
                    "volume_24h_usd":       bitcoin["usd_24h_vol"],
                    "price_change_24h_pct": bitcoin["usd_24h_change"],
                }

                self._price_cache = result
                self._cache_time  = time.monotonic()
                return result

        if self._price_cache is not None:
            return self._price_cache

        raise RuntimeError("CoinGecko rate limit exceeded after retries, no cached price available")

    async def close(self):
        pass