# Saturn

**Sentiment-driven AI Trading & Unified Recommendation Network**

Saturn is a full-stack Bitcoin trading decision making platform. It ingests crypto news from multiple RSS feeds, scores each headline using FinBERT (a financial-domain BERT model), aggregates sentiment into a BUY/SELL/HOLD signal with confidence percentage, and displays everything on a real-time terminal-style dashboard. A streaming AI explanation panel powered by Groq gives plain-English breakdowns of the current signal.

---

## Features

- **Live sentiment pipeline** — 5 RSS feeds ingested every 10 minutes via APScheduler
- **FinBERT scoring** — local HuggingFace model, no API cost per headline
- **Signal engine** — aggregates positive/neutral/negative counts into a BUY/SELL/HOLD signal with confidence score
- **Real-time dashboard** — three-column terminal UI: signal & sentiment left, price chart & AI centre, live feed right
- **Streaming AI analysis** — `/ai/explain` endpoint streams a Groq (Llama 3.1 8B) plain-English breakdown of the active signal
- **MCP server** — stdio-based Model Context Protocol server for AI agent integration

---

## Architecture

![alt text](<Saturn Architecture-1.png>)

## Tech Stack

### Backend

Framework - FastAPI (async) 
Database - MongoDB Atlas via Motor (async driver) 
Sentiment model - FinBERT (ProsusAI/finbert, HuggingFace Transformers) 
Scheduling - APScheduler 
Feed parsing - feedparser
HTTP client - httpx (async) 
AI explanation - Groq API — Llama 3.1 8B Instant (free tier) 
Agent protocol - MCP (stdio) 
Language - Python 3.13 

### Frontend

Framework - React 19 + Vite 
Charts - Recharts 
HTTP client - Axios 
Styling - Plain CSS with CSS custom properties 
Fonts - Chonburi, Domine, JetBrains Mono 

---

## Project Structure
AI-BTC-Trader/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py              # Pydantic settings
│   │   │   └── database.py            # MongoDB async client
│   │   ├── mcp/
│   │   │   ├── server.py              # MCP stdio server
│   │   │   └── tools.py               # MCP tool definitions
│   │   ├── models/
│   │   │   ├── price.py
│   │   │   ├── sentiment.py
│   │   │   └── signal.py
│   │   ├── repositories/
│   │   │   ├── base.py
│   │   │   ├── sentiment_repository.py
│   │   │   └── signal_repository.py
│   │   ├── routers/
│   │   │   ├── ai.py                  # /ai/explain streaming endpoint
│   │   │   ├── price.py
│   │   │   ├── sentiment.py
│   │   │   └── signals.py
│   │   ├── services/
│   │   │   ├── ingestion_service.py   # RSS feed ingestion
│   │   │   ├── sentiment_service.py   # FinBERT analysis
│   │   │   └── signal_service.py      # Signal generation
│   │   └── main.py                    # FastAPI entry point
│   ├── scheduler/
│   │   └── jobs.py                    # APScheduler jobs
│   ├── tests/
│   ├── requirements.txt
│   ├── .env.example
│   └── .venv/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── FeedList.jsx           # Live news feed, right column
│   │   │   ├── PriceChart.jsx         # BTC/USD 24h chart
│   │   │   ├── SentimentGauge.jsx     # Bullish/Neutral/Bearish breakdown
│   │   │   └── SignalBadge.jsx        # Active BUY/SELL/HOLD signal
│   │   ├── hooks/
│   │   │   ├── useSentiment.js
│   │   │   └── useSignal.js
│   │   ├── pages/
│   │   │   └── Dashboard.jsx          # Three-column layout
│   │   ├── services/
│   │   │   └── api.js                 # Axios API client
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   ├── index.css                  # CSS variables & global reset
│   │   ├── dashboard.css              # Layout & structural styles
│   │   └── components/
│   │       └── components.css         # Component-level styles
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
├── LICENSE
└── README.md

---

## Getting Started

### Prerequisites
- Python 3.13
- Node.js 18+
- MongoDB Atlas account (or local MongoDB instance)
- Groq API key (free tier at console.groq.com)

### Backend Setup

1. **Clone the repo**:
```bash
   git clone https://github.com/YOUR_USERNAME/AI-BTC-Trader.git
   cd AI-BTC-Trader/backend
```

2. **Create virtual environment**:
```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\Activate.ps1
   # macOS/Linux:
   source .venv/bin/activate
```

3. **Install dependencies**:
```bash
   pip install -r requirements.txt
```

4. **Configure environment**:
```bash
   cp .env.example .env
   # Fill in MONGODB_URI, GROQ_API_KEY, and other values
```

5. **Run the backend**:
```bash
   uvicorn app.main:app --reload
```
   Runs on `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend**:
```bash
   cd ../frontend
```

2. **Install dependencies**:
```bash
   npm install
```

3. **Set API URL**:
```bash
   echo "VITE_API_URL=http://localhost:8000" > .env.local
```

4. **Run development server**:
```bash
   npm run dev
```
   Runs on `http://localhost:5173`

---

## API Endpoints

GET | `/sentiment/latest` | Latest sentiment record 
GET | `/sentiment/feed?limit=25` | Paginated sentiment feed 
GET | `/signals/latest` | Latest BUY/SELL/HOLD signal 
GET | `/signals/feed?limit=10` | Signal history 
GET | `/price/btc` | Current BTC price, 24h change, market cap 
GET | `/price/btc/history` | 24h price history for chart 
GET | `/pipeline/trigger` | Manually trigger ingestion pipeline 
GET | `/ai/explain` | Streaming AI explanation of active signal 

---

## Architecture

### Data Pipeline
RSS Feeds (5 sources, 10 min interval)
↓ feedparser
FinBERT sentiment scoring (local, no API cost)
↓
Signal engine → BUY / SELL / HOLD + confidence
↓
MongoDB Atlas (sentiments / signals / prices collections)
↓
FastAPI REST + /ai/explain streaming
↓
React Dashboard            MCP stdio server
(browser)                  (AI agents / Claude Desktop)

### Dual AI Layer
Saturn has two separate AI-powered interfaces sharing the same data layer:

- **HTTP** — `/ai/explain` streams a Groq-powered plain-English breakdown of the current signal directly into the dashboard
- **MCP stdio** — exposes the same signal and sentiment data as MCP tools, allowing Claude Desktop or any MCP-compatible agent to query Saturn programmatically

---

## Configuration

All configuration via `.env` in `backend/`:

```env
# MongoDB
MONGODB_URI=mongodb+srv://user:password@cluster.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB_NAME=btc_sentiment

# Groq (AI explanation)
GROQ_API_KEY=your_groq_api_key

# CoinGecko
COINGECKO_BASE_URL=https://api.coingecko.com/api/v3

# Pipeline interval (minutes)
SCHEDULER_INTERVAL_MINUTES=10
```

---

## Development Notes

**Adding RSS feeds** — edit `RSS_FEEDS` list in `backend/app/services/ingestion_service.py`.

**Swapping the sentiment model** — modify `backend/app/services/sentiment_service.py`. Any HuggingFace classification model works as a drop-in.

**Adding API endpoints** — create a router in `backend/app/routers/` and register it in `backend/app/main.py`.

**CSS architecture** — three files in order of cascade: `index.css` (variables & reset) → `dashboard.css` (layout) → `components/components.css` (component styles). All three are imported in `App.jsx`.

---

## Testing

```bash
cd backend
pytest tests/
# verbose:
pytest tests/ -v
```

---

## Roadmap

- [x] RSS ingestion pipeline
- [x] FinBERT sentiment scoring
- [x] Signal generation engine
- [x] FastAPI backend with 8 endpoints
- [x] React terminal dashboard
- [x] Streaming AI explanation panel
- [x] MCP server (stdio)
- [ ] Frontend testing (DevTools network audit)
- [ ] Deployment — backend to Render, frontend to Vercel

---

## Disclaimer

**This tool is for educational and research purposes only.** It is not financial advice. Cryptocurrency markets are highly volatile. Never invest more than you can afford to lose.

---

## Contributors are welcome

## License

MIT — see [LICENSE](LICENSE) for details.