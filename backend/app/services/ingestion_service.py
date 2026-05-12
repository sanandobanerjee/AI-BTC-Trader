import asyncio
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


class RSSNewsClient:

    def get_btc_posts(self, limit: int = 25) -> list[dict]:
        results = []
        per_feed = max(1, limit // len(RSS_FEEDS))

        for feed_url in RSS_FEEDS:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:per_feed]:
                    title = entry.get("title", "").strip()
                    summary = entry.get("summary", "").strip()
                    if not title:
                        continue
                    text = f"{title}. {summary[:150]}".strip()
                    results.append({
                        "text": text,
                        "source": "rss",
                    })
            except Exception:
                continue

        return results[:limit]


class IngestionService:

    def __init__(self):
        self.rss_client = RSSNewsClient()

    async def fetch_news(self, limit: int = 25) -> list[dict]:
        loop = asyncio.get_event_loop()
        posts = await loop.run_in_executor(
            None,
            lambda: self.rss_client.get_btc_posts(limit=limit),
        )
        return posts

    async def fetch_price(self) -> dict:
        url = f"{settings.COINGECKO_BASE_URL}/simple/price"
        params = {
            "ids": "bitcoin",
            "vs_currencies": "usd",
            "include_market_cap": "true",
            "include_24hr_vol": "true",
            "include_24hr_change": "true",
        }
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            bitcoin = data["bitcoin"]
            return {
                "price_usd": bitcoin["usd"],
                "market_cap_usd": bitcoin["usd_market_cap"],
                "volume_24h_usd": bitcoin["usd_24h_vol"],
                "price_change_24h_pct": bitcoin["usd_24h_change"],
            }

    async def close(self):
        pass