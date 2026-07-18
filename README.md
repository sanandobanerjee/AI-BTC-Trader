<div align="center">

# ◈ $aturn

### Sentiment-driven AI Trading & Unified Recommendation Network

*Real-time Bitcoin intelligence powered by FinBERT, Groq, and a live RSS pipeline*

[![FastAPI](https://img.shields.io/badge/FastAPI-0.135-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-19-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?style=flat-square&logo=mongodb&logoColor=white)](https://mongodb.com)
[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-f7931a?style=flat-square)](LICENSE)

</div>

<br>

Saturn is a full-stack Bitcoin intelligence platform that turns live crypto news into actionable trading signals. It ingests headlines from multiple RSS feeds, scores each one using FinBERT, aggregates the sentiment into a BUY / SELL / HOLD recommendation with a confidence score, and displays everything in a real-time terminal-style dashboard. A streaming AI layer powered by Groq also explains the current signal in plain English.

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

- **Live sentiment pipeline** — RSS feeds are ingested on a recurring schedule via APScheduler
- **FinBERT scoring** — financial-domain sentiment analysis through Hugging Face Inference API
- **Signal engine** — aggregates positive, neutral, and negative counts into a BUY / SELL / HOLD signal with confidence
- **Real-time dashboard** — a three-column terminal UI for signal status, price movement, and live feed data
- **Streaming AI analysis** — the `/ai/explain` endpoint streams a Groq-powered market explanation in real time
- **MCP server** — stdio-based integration for Claude Desktop and other MCP-compatible agents

---

## Dashboard

<div align="center">

<img src="https://res.cloudinary.com/hlwsik4u/image/upload/v1784217027/Saturn_Look_May_26_amxfaq.jpg" alt="Saturn dashboard preview" width="900" />

</div>

---

## Architecture

Saturn is built using the SOLID principles as a guideline. All the ideas provided in the SOLID framework are implemented as cleanly as possible.
The app is constructed as a modular pipeline that moves from ingestion to insight:

1. RSS feeds are collected and normalized into article-like payloads.
2. Each article is scored by FinBERT for sentiment polarity and confidence.
3. The backend aggregates the results into a structured trading signal.
4. The frontend renders the signal, price insight, and live feed in a terminal-inspired dashboard.
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
- **Sentiment model** — FinBERT via Hugging Face Inference API
- **Scheduling** — APScheduler
- **Feed parsing** — feedparser
- **HTTP client** — httpx
- **AI explanation** — Groq API with Llama 3.1 8B Instant
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
│   │   ├── core/
│   │   ├── mcp/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── routers/
│   │   ├── services/
│   │   └── main.py
│   ├── scheduler/
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
| GET | `/sentiment/latest` | Latest sentiment record |
| GET | `/sentiment/feed?limit=25` | Paginated sentiment feed |
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
COINGECKO_BASE_URL=https://api.coingecko.com/api/v3
FRONTEND_URL=http://localhost:5173
```

---

## Testing

```bash
cd backend
pytest tests/
```

---

## Roadmap

A list of ideas which can be implemented after deployment:

-> Integrating other cryptocurrency markets
-> Higher source transparency
-> Integrating the Indian Stock market
-> Higher information ingestion for better results

---

## Disclaimer

This project is for educational and research purposes only. It is not financial advice. Cryptocurrency markets are highly volatile, so never invest more than you can afford to lose.

---

## License

MIT — see [LICENSE](LICENSE) for details.