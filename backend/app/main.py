import logging
import logging.config
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import connect_db, close_db
from app.routers import sentiment, signals, price
from scheduler.jobs import start_scheduler, stop_scheduler
from app.api.routes.ai import router as ai_router
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).parent.parent/".env")

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"]
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application starting up")
    await connect_db()
    start_scheduler()
    logger.info("Application ready")
    yield
    logger.info("Application shutting down")
    stop_scheduler()
    await close_db()
    logger.info("Application stopped")

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

app = FastAPI(
    title="BTC Sentiment Trader",
    description="AI bitcoin sentiment trading signals",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://your-frontend.vercel.app",
        FRONTEND_URL,
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(sentiment.router)
app.include_router(signals.router)
app.include_router(price.router)
app.include_router(ai_router)

@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok", "version": "1.0.0"}