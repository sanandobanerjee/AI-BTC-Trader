import json
import logging
from mcp.server.models import InitializationOptions
from mcp.types import Tool,TextContent
from app.mcp.server import app
from app.core.database import get_database
from app.repositories.sentiment_repository import SentimentRepository
from app.repositories.signal_repository import SignalRepository
from app.services.signal_service import SignalService

logger=logging.getLogger(__name__)

@app.list_tools()
async def list_tools()->list[Tool]:
    return[
        Tool(
            name="get_current_signal",
            description=(
                "Returns the most recent BUY, SELL,HOLD trading signal "
                "for Bitcoin based on sentiment analysis."
                "Includes confidence score and sentiment breakdown."
            ),
            inputSchema={
                "type":"object",
                "properties":{},
                "required":[]
            },
        ),
        Tool(
            name="get_sentiment_feed",
            description=(
                "Returns a list of recent Bitcoin sentiment records scored "
                "by Finbert. Each record includes the source"
                "positive/negative/neutral, and confidence score."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Number of records to return: Minimum is 10 & Maximum is 50.",
                        "default": 10,
                    }
                },
                "required":[],
            },
        ),
    ]

@app.call_tool()
async def call_tool(name:str,arguments:dict) -> list[TextContent]:
    db=get_database()

    if name== "get_current_signal":
        return await _handle_get_current_signal(db)
    
    if name=="get_sentiment_feed":
        limit=min(int(arguments.get("limit",10)),50)
        return await _handle_get_sentiment_feed(db,limit)
    
    return [TextContent(
        type="text",
        text=json.dumps({"error": f"Unknown: {name}"})
    )]

async def _handle_get_current_signal(db)-> list[TextContent]:
    sentiment_repo=SentimentRepository(db)
    signal_repo=SignalRepository(db)
    signal_service=SignalService(
        sentiment_repository=sentiment_repo,
        signal_repository=sentiment_repo
    )
    signal = await signal_service.get_latest()

    if not signal:
        result={"error":"No signal available yet.Pipeline may not have run."}
    else:
        result={
            "signal":signal.signal,
            "confidence": signal.confidence,
            "avg_sentiment_score": signal.avg_sentiment_score,
            "positive_count": signal.positive_count,
            "negative_count": signal.negative_count,
            "neutral_count": signal.neutral_count,
            "sample_size": signal.sample_size,
            "created_at": signal.created_at.isoformat()
        }
    return [TextContent(type="text",text=json.dumps(result,indent=2))]

async def _handle_get_sentiment_feed(db,limit:int)-> list[TextContent]:
    sentiment_repo=SentimentRepository(db)

    records=await sentiment_repo.find_many(limit=limit)

    if not records:
        result={"error":"No sentiment records found. Pipeline may not have run"}
    else:
        result = {
            "count": len(records),
            "records": [
                {
                    "source": r.source,
                    "label": r.label,
                    "score": r.score,
                    "raw_text": r.raw_text[:120], #truncation for context window of agent
                    "created_at": r.created_at.isoformat(),
                } 
                for r in records
            ],
        }

    return [TextContent(type="text",text=json.dumps(result,indent=2))]