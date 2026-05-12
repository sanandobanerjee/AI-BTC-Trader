import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.core.database import get_database
from app.repositories.sentiment_repository import SentimentRepository
from app.repositories.signal_repository import SignalRepository
from app.services.ingestion_service import IngestionService
from app.services.sentiment_service import SentimentService
from app.services.signal_service import SignalService
from app.models.price import PriceSnapshot

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


async def run_pipeline():
    logger.info("Pipeline started")

    db = get_database()
    sentiment_repo = SentimentRepository(db)
    signal_repo = SignalRepository(db)

    ingestion_service = IngestionService()
    sentiment_service = SentimentService(repository=sentiment_repo)
    signal_service = SignalService(
        sentiment_repository=sentiment_repo,
        signal_repository=signal_repo,
    )

    try:
        posts = await ingestion_service.fetch_news(limit=25)
        logger.info(f"Fetched {len(posts)} posts from RSS")

        records = await sentiment_service.analyse_batch(posts)
        logger.info(f"Scored {len(records)} sentiment records")

        signal = await signal_service.compute_and_store(sample_size=20)
        logger.info(f"Signal computed: {signal.signal} (confidence: {signal.confidence})")

    except Exception as e:
        logger.error(f"Sentiment pipeline failed: {e}", exc_info=True)

    try:
        price_data = await ingestion_service.fetch_price()
        price_snapshot = PriceSnapshot(**price_data)
        payload = price_snapshot.model_dump()
        payload["_id"] = payload.pop("id")
        db_price = db["prices"]
        await db_price.insert_one(payload)
        logger.info(f"Price snapshot stored: ${price_snapshot.price_usd:,.2f}")

    except Exception as e:
        logger.error(f"Price fetch failed: {e}", exc_info=True)

    finally:
        await ingestion_service.close()


def start_scheduler():
    scheduler.add_job(
        func=run_pipeline,
        trigger=IntervalTrigger(minutes=10),
        id="btc_pipeline",
        name="BTC Sentiment Pipeline",
        replace_existing=True,
        max_instances=1,
    )
    scheduler.start()
    logger.info("Scheduler started - Pipeline runs every 10 minutes")


def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("Scheduler stopped")