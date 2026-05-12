import logging
from mcp.server import Server
from mcp.server.stdio import stdio_server
from app.core.database import connect_db,close_db

logger=logging.getLogger(__name__)

app=Server("btc-sentiment-trader")

async def run_mcp_server():
    logger.info("MCP Server Starting...")
    await connect_db()
    try:
        async with stdio_server() as (read_stream, write_stream):
            await app.run(
                read_stream,
                write_stream,
                app.create_initialization_options()
            )
    finally:
        await close_db()
        logger.info("MCP Server Stopped")