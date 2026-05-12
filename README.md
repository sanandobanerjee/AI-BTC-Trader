# AI-BTC-Trader

An AI-powered Bitcoin trading bot that combines sentiment analysis with technical signal generation to identify and evaluate trading opportunities.

## Overview

AI-BTC-Trader is a full-stack application that:
- **Ingests Bitcoin news** from multiple RSS feeds (CoinDesk, Cointelegraph, Decrypt, Bitcoin Magazine, CryptoSlate)
- **Analyzes sentiment** using FinBERT (a financial domain-specific BERT model) to understand market sentiment
- **Generates trading signals** based on sentiment trends and market conditions
- **Provides a real-time dashboard** to visualize price, sentiment, and trading signals
- **Exposes an MCP server** for AI agent integration and extensibility (currently in development)

## Tech Stack

### Backend
- **Framework**: FastAPI with async/await support
- **Database**: MongoDB (async driver: Motor)
- **ML/NLP**: Transformers (FinBERT for sentiment analysis)
- **Job Scheduling**: APScheduler (runs sentiment analysis pipeline)
- **API Integration**: HTTPx (async HTTP client)
- **Server Protocol**: MCP (Model Context Protocol)
- **Language**: Python 3.10+

### Frontend
- **Framework**: React 19 with Vite
- **UI Components**: Recharts (data visualization)
- **HTTP Client**: Axios
- **Styling**: CSS
- **Dev Tools**: ESLint

## Project Structure

```
AI-BTC-Trader/
├── backend/                          # Python FastAPI backend
│   ├── app/
│   │   ├── core/                     # Core configs and DB setup
│   │   │   ├── config.py             # Pydantic settings
│   │   │   └── database.py           # MongoDB async client
│   │   ├── mcp/                      # MCP server integration
│   │   │   ├── server.py
│   │   │   └── tools.py
│   │   ├── models/                   # Pydantic models
│   │   │   ├── price.py
│   │   │   ├── sentiment.py
│   │   │   └── signal.py
│   │   ├── repositories/             # Data access layer
│   │   │   ├── base.py               # Abstract repository
│   │   │   ├── sentiment_repository.py
│   │   │   └── signal_repository.py
│   │   ├── routers/                  # API endpoints
│   │   │   ├── price.py
│   │   │   ├── sentiment.py
│   │   │   └── signals.py
│   │   ├── services/                 # Business logic
│   │   │   ├── ingestion_service.py  # RSS feed ingestion
│   │   │   ├── sentiment_service.py  # FinBERT analysis
│   │   │   └── signal_service.py     # Signal generation
│   │   └── main.py                   # FastAPI app entry point
│   ├── scheduler/
│   │   └── jobs.py                   # Scheduled tasks (APScheduler)
│   ├── tests/                        # Unit & integration tests
│   ├── requirements.txt              # Python dependencies
│   ├── .env.example                  # Environment template
│   └── .venv/                        # Virtual environment (git-ignored)
│
├── frontend/                         # React + Vite frontend
│   ├── src/
│   │   ├── components/               # React components
│   │   │   ├── FeedList.jsx
│   │   │   ├── PriceChart.jsx
│   │   │   ├── SentimentGauge.jsx
│   │   │   └── SignalBadge.jsx
│   │   ├── hooks/                    # Custom React hooks
│   │   │   ├── useSentiment.js
│   │   │   └── useSignal.js
│   │   ├── pages/
│   │   │   └── Dashboard.jsx
│   │   ├── services/
│   │   │   └── api.js                # API client
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.js
│   └── node_modules/                 # Dependencies (git-ignored)
│
├── .gitignore
├── LICENSE                           # MIT License
└── README.md                         # This file
```

## Getting Started

### Prerequisites
- Python 3.10+ (for backend)
- Node.js 18+ (for frontend)
- MongoDB Atlas account (or local MongoDB instance)

### Backend Setup

1. **Clone and navigate to backend**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/AI-BTC-Trader.git
   cd AI-BTC-Trader/backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your MongoDB URI and other credentials
   ```

5. **Run the backend**:
   ```bash
   uvicorn app.main:app --reload
   ```
   Backend runs on `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend**:
   ```bash
   cd ../frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Create environment file** (if needed):
   ```bash
   echo "VITE_API_URL=http://localhost:8000" > .env.local
   ```

4. **Run development server**:
   ```bash
   npm run dev
   ```
   Frontend runs on `http://localhost:5173`

## API Endpoints

### Sentiment Analysis
- `GET /sentiment/latest` - Get latest sentiment records
- `GET /sentiment/feed?limit=25` - Get sentiment feed

### Trading Signals
- `GET /signals/latest` - Get latest trading signals
- `GET /signals/feed?limit=10` - Get signal feed

### Price Data
- `GET /price/btc` - Get current BTC price

## Architecture

### Data Pipeline
1. **Ingestion**: APScheduler periodically fetches RSS feeds from multiple sources
2. **Sentiment Analysis**: Each news article is tokenized and classified using FinBERT
3. **Signal Generation**: Trading signals are generated based on aggregate sentiment and market conditions
4. **Storage**: All data is persisted in MongoDB
5. **API**: FastAPI exposes endpoints for frontend consumption
6. **UI**: React dashboard visualizes real-time data

### Key Components

**FinBERT Model**: Pre-trained on financial domain text, performs better than general-purpose models for cryptocurrency sentiment

**APScheduler**: Runs the sentiment analysis pipeline at configurable intervals, ensuring data freshness

**Motor**: Async MongoDB driver enabling non-blocking database operations

**MCP Server**: Enables AI agents to query trading signals and sentiment data programmatically

## Configuration

All configuration is managed via environment variables in `.env`:

```env
# MongoDB
MONGODB_URI=mongodb+srv://user:password@cluster.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB_NAME=btc_sentiment

# External APIs
COINGECKO_BASE_URL=https://api.coingecko.com/api/v3
```

## Testing

Run tests with pytest:
```bash
cd backend
pytest tests/
```

For async tests:
```bash
pytest tests/ -v
```

## Development

### Adding New RSS Feeds
Edit `backend/app/services/ingestion_service.py` and add URLs to `RSS_FEEDS` list.

### Customizing Sentiment Model
Modify `backend/app/services/sentiment_service.py` to use different models from Hugging Face.

### Adding New API Endpoints
Create new routers in `backend/app/routers/` and import them in `backend/app/main.py`.

## Deployment
(Coming Soon)

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

**This tool is for educational and research purposes only.** It is not financial advice. Cryptocurrency trading is risky. Always do your own research and never invest more than you can afford to lose.

## Support

For issues, questions, or suggestions, please [open an issue](https://github.com/YOUR_USERNAME/AI-BTC-Trader/issues) on GitHub.

## Roadmap

1) MCP Server Integration
2) Frontend Component Changes
3) Deployment



---

