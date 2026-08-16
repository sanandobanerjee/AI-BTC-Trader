[![E2E Tests](https://github.com/sanandobanerjee/Saturn-AI/actions/workflows/e2e-tests.yml/badge.svg)](https://github.com/sanandobanerjee/Saturn-AI/actions/workflows/e2e-tests.yml)

<div align="center">

# ◈ $aturn ◈ 

### Sentiment-driven AI Trading & Unified Recommendation Network

*Real-time Bitcoin intelligence powered by Groq, RSS ingestion, and BTC price tracking*

[![FastAPI](https://img.shields.io/badge/FastAPI-0.135-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-19-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?style=flat-square&logo=mongodb&logoColor=white)](https://mongodb.com)
[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-f7931a?style=flat-square)](LICENSE)

</div>

<br>

Saturn is a full-stack Bitcoin intelligence platform that turns live crypto news into actionable trading signals. It ingests headlines from multiple RSS feeds, classifies them with a Groq-powered sentiment model, aggregates the results into a BUY / SELL / HOLD recommendation with a confidence score and sample breakdown, and displays everything in a React dashboard. The backend also runs a recurring pipeline every 10 minutes to refresh signals, collect recent BTC price history, and stream a plain-English AI explanation of the latest recommendation.

<br>

<div align="center">

<table>
  <tr>
    <td align="center"><strong>Live RSS Ingestion</strong><br>Five news sources, scheduled continuously</td>
    <td align="center"><strong>Sentiment Scoring</strong><br>FinBERT-driven analysis for market tone</td>
    <td align="center"><strong>AI Explanation</strong><br>Groq-generated plain-English signal summaries</td>
  </tr>
</table>

</div>

---

## Features

- **Live sentiment pipeline** — RSS feeds are ingested on a recurring schedule via APScheduler, with the pipeline refreshing every 10 minutes
- **Groq-powered sentiment scoring** — headlines are classified with a Groq LLM and stored as sentiment records with confidence scores
- **Signal engine** — aggregates positive, neutral, and negative counts into a BUY / SELL / HOLD signal with confidence and sample breakdown
- **Live BTC price tracking** — price snapshots and recent history are fetched from CoinGecko and shown in the dashboard
- **React dashboard** — a live UI for signal status, price movement, recent headlines, and AI analysis
- **Streaming AI analysis** — the `/ai/explain` endpoint streams a Groq-powered market explanation in real time
- **MCP server** — stdio-based integration for Claude Desktop and other MCP-compatible agents
- **Playwright E2E testing** — automated end-to-end tests for the React dashboard with Playwright
- **GitHub Actions CI/CD** — automated E2E test pipeline that runs on every push to ensure code quality

---

## Dashboard

<div align="center">

<img src="https://res.cloudinary.com/hlwsik4u/image/upload/v1784217027/Saturn_Look_May_26_amxfaq.jpg" alt="Saturn dashboard preview" width="900" />

</div>

---

## Architecture

Saturn is built using the SOLID principles as a guideline. Recent changes added a scheduled background job for recurring updates, a dedicated price-history layer, and a streaming AI explanation endpoint while keeping the backend modular and easier to extend.
The app is constructed as a modular pipeline that moves from ingestion to insight:

1. RSS feeds are collected and normalized into article-like payloads.
2. Each article is classified by a Groq-based sentiment model for label and confidence.
3. The backend aggregates the results into a structured trading signal.
4. The frontend renders the signal, price insight, and recent news feed in a React dashboard.
5. A streaming AI endpoint explains the active signal in natural language.

### Architecture Diagram

```mermaid
flowchart LR
    A[RSS feeds] --> B[Feed ingestion]
    B --> C[FinBERT scoring]
    C --> D[Signal engine]
    D --> E[(MongoDB Atlas)]
    D --> F[FastAPI API]
    F --> G[React dashboard]
    F --> H[MCP server]
    G --> I[AI explanation]
```

### Dual AI Layer

Saturn exposes two AI-powered interfaces over the same data layer:

- **HTTP streaming** — `/ai/explain` streams a Groq-powered plain-English breakdown directly into the dashboard
- **MCP stdio** — exposes signal and sentiment data as tools for Claude Desktop or any MCP-compatible agent

---

## Tech Stack

### Backend

- **Framework** — FastAPI (async)
- **Database** — MongoDB Atlas via Motor
- **Sentiment model** — Groq API with OpenAI OSS 20B
- **Scheduling** — APScheduler for recurring ingestion and signal refreshes
- **Feed parsing** — feedparser
- **Price data** — CoinGecko API for BTC price snapshots and history
- **HTTP client** — httpx
- **AI explanation** — Groq API streaming responses
- **Agent protocol** — MCP (stdio)
- **Language** — Python 3.13

### Frontend

- **Framework** — React 19 + Vite
- **Charts** — Recharts
- **HTTP client** — Axios
- **Styling** — Plain CSS with custom properties
- **Fonts** — Chonburi, Domine, JetBrains Mono

---

## Project Structure

<details>
<summary>View repository layout</summary>

```text
Saturn-AI/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   ├── core/
│   │   ├── mcp/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── routers/
│   │   ├── services/
│   │   └── main.py
│   ├── scheduler/
│   │   └── jobs.py
│   ├── tests/
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   ├── index.css
│   │   ├── dashboard.css
│   │   └── components.css
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
├── LICENSE
└── README.md
```

</details>

---

## Getting Started

### Prerequisites

- Python 3.13
- Node.js 18+
- MongoDB Atlas account or a local MongoDB instance
- Groq API key (free tier at console.groq.com)

### Backend Setup

1. Clone the repository:
```bash
git clone https://github.com/sanandobanerjee/Saturn-AI.git
cd AI-BTC-Trader/backend
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
# Windows:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
```

5. Run the backend:
```bash
uvicorn app.main:app --reload
```

### Frontend Setup

1. Navigate to the frontend folder:
```bash
cd ../frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set the API URL:
```bash
echo "VITE_API_URL=http://localhost:8000" > .env.local
```

4. Start the development server:
```bash
npm run dev
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Backend health check |
| GET | `/sentiment/latest` | Latest sentiment record |
| GET | `/sentiment/feed?limit=25` | Paginated sentiment feed |
| GET | `/sentiment/feed/{source}` | Sentiment feed filtered by source |
| GET | `/signals/current` | Current BUY / SELL / HOLD signal |
| GET | `/signals/history` | Signal history |
| GET | `/price/btc` | Current BTC price, 24h change, and market cap |
| GET | `/price/btc/history` | Recent price history for charting |
| POST | `/signals/trigger` | Manually trigger the ingestion pipeline |
| GET | `/ai/explain` | Streaming AI explanation of the active signal |

---

## Configuration

All configuration is handled through environment variables in the backend:

```env
MONGODB_URI=mongodb+srv://user:password@cluster.mongodb.net/
MONGODB_DB_NAME=btc_sentiment
GROQ_API_KEY=your_groq_api_key
HUGGINGFACE_API_KEY=your_huggingface_key
COINGECKO_BASE_URL=https://api.coingecko.com/api/v3
FRONTEND_URL=http://localhost:5173
CORS_ALLOW_ALL=false
SENTIMENT_TTL_DAYS=45
SIGNAL_TTL_BUFFER_HOURS=12
```

---

## Testing

```bash
cd backend
pytest tests/
```

---

## Roadmap

Features which are coming soon:

1. Signal outcome tracking / backtesting loop 
2. Backend tests using pytest
3. Multi-asset support (ETH, SOL)
4. Structured logging 
5. Historical signal browsing UI
6. Email alerting on signal change

---

## Disclaimer

This project is for educational and research purposes only. It is not financial advice. Cryptocurrency markets are highly volatile, so never invest more than you can afford to lose.

---

## License

MIT — see [LICENSE](LICENSE) for details.