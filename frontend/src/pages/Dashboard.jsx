import { useState, useRef } from "react"
import { useSignal } from "../hooks/useSignal"
import { useSentiment } from "../hooks/useSentiment"
import SignalBadge from "../components/SignalBadge"
import SentimentGauge from "../components/SentimentGauge"
import PriceChart from "../components/PriceChart"
import FeedList from "../components/FeedList"

function StatCard({ label, value, sub, valueClass }) {
  return (
    <div className="stat-card">
      <div className="stat-card__label">{label}</div>
      <div className={`stat-card__value ${valueClass || ""}`}>{value}</div>
      {sub && <div className="stat-card__sub">{sub}</div>}
    </div>
  )
}

function Dashboard() {
  const {
    signal, price, priceHistory,
    loading: signalLoading, error: signalError,
    lastUpdated, triggerPipeline,
  } = useSignal()

  const { feed, loading: sentimentLoading, error: sentimentError } = useSentiment(30)

  const [aiText, setAiText]       = useState("")
  const [aiLoading, setAiLoading] = useState(false)
  const [aiError, setAiError]     = useState("")
  const abortRef                  = useRef(null)

  const isLoading    = signalLoading || sentimentLoading
  const errorMessage = signalError || sentimentError

const API_BASE = (import.meta.env.VITE_API_URL || "http://localhost:8000").replace(/\/$/, "")

async function handleExplain() {
    setAiText("")
    setAiError("")
    setAiLoading(true)
    abortRef.current = new AbortController()
    try {
      const res = await fetch(
        `${API_BASE}/ai/explain`,
        { signal: abortRef.current.signal }
      )
      if (!res.ok) {
        const err = await res.json()
        throw new Error(err.detail || "Failed to fetch analysis")
      }
      const reader  = res.body.getReader()
      const decoder = new TextDecoder()
      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        setAiText(prev => prev + decoder.decode(value, { stream: true }))
      }
    } catch (err) {
      if (err.name !== "AbortError") setAiError(err.message)
    } finally {
      setAiLoading(false)
    }
  }
  
  function handleAbort() {
    abortRef.current?.abort()
    setAiLoading(false)
  }

  function formatMarketCap(v) {
    if (!v) return "-"
    if (v >= 1e12) return "$" + (v / 1e12).toFixed(2) + "T"
    if (v >= 1e9)  return "$" + (v / 1e9).toFixed(2) + "B"
    return "$" + v.toLocaleString()
  }

  const priceChangeClass = price?.price_change_24h_pct >= 0
    ? "stat-card__value--positive"
    : "stat-card__value--negative"

  return (
    <div className="app-shell">

      {/* ── Header ── */}
      <header className="header">
        <div className="header__brand">
          <h1 className="header__title">$aturn</h1>
          <span className="header__subtitle">
            Sentiment-driven AI Trading &amp; Unified Recommendation Network
          </span>
        </div>
        <div className="header__status">
          <div className="header__live">
            <span className="header__live-dot" />
            Live
          </div>
          {lastUpdated && (
            <span className="header__updated">
              Updated {lastUpdated.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
            </span>
          )}
        </div>
        <div className="header__actions">
          <button
            className="header__refresh-btn"
            onClick={triggerPipeline}
            disabled={isLoading}
          >
            {isLoading ? "Running..." : "↻ Refresh Signal"}
          </button>
        </div>
      </header>

      {/* ── Terminal Grid ── */}
      <main className="terminal-grid">

        {errorMessage && (
          <div className="error-banner">{errorMessage}</div>
        )}

        {/* Left Column */}
        <div className="col-left">
          <SignalBadge signal={signal?.signal} confidence={signal?.confidence} />
          <SentimentGauge
            positiveCount={signal?.positive_count}
            negativeCount={signal?.negative_count}
            neutralCount={signal?.neutral_count}
            sampleSize={signal?.sample_size}
          />
          <div className="stat-grid">
            <StatCard
              label="BTC Price"
              value={price ? "$" + price.price_usd.toLocaleString() : "-"}
              valueClass="stat-card__value--brand"
            />
            <StatCard
              label="24h Change"
              value={
                price
                  ? (price.price_change_24h_pct >= 0 ? "+" : "") +
                    price.price_change_24h_pct?.toFixed(2) + "%"
                  : "-"
              }
              valueClass={priceChangeClass}
            />
            <StatCard
              label="Market Cap"
              value={formatMarketCap(price?.market_cap_usd)}
            />
            <StatCard
              label="Avg Sentiment"
              value={
                signal?.avg_sentiment_score != null
                  ? (signal.avg_sentiment_score * 100).toFixed(1) + "%"
                  : "-"
              }
              sub={`${signal?.sample_size ?? 0} articles`}
            />
          </div>
        </div>

        {/* Centre Column */}
        <div className="col-centre">
          <div className="panel chart-panel">
            <div className="panel__header">
              <span className="panel__title">Price Chart</span>
            </div>
            <PriceChart priceHistory={priceHistory} />
          </div>

          <div className="panel ai-panel">
            <div className="panel__header">
              <span className="panel__title">✦ Saturn AI Intelligence</span>
              {aiLoading && (
                <span style={{ fontSize: 10, fontFamily: "var(--mono)", color: "var(--buy)" }}>
                  ● Analysing...
                </span>
              )}
              {aiError && (
                <span style={{ fontSize: 10, fontFamily: "var(--mono)", color: "var(--sell)" }}>
                  {aiError}
                </span>
              )}
            </div>
            <div className="ai-panel__body">
              {aiText ? (
                <p className="ai-panel__output">
                  {aiText}
                  {aiLoading && <span className="ai-panel__cursor" />}
                </p>
              ) : (
                <p className="ai-panel__placeholder">
                  {aiLoading
                    ? "Generating analysis..."
                    : "Click below to get a plain-English breakdown of the current signal."}
                </p>
              )}
            </div>
            <div className="ai-panel__footer">
              <button
                className={`ai-panel__btn ${aiLoading ? "ai-panel__btn--stop" : ""}`}
                onClick={aiLoading ? handleAbort : handleExplain}
                disabled={!signal}
              >
                {aiLoading ? "⏹ Stop Analysis" : "✦ Ask Saturn AI"}
              </button>
            </div>
          </div>
        </div>

        {/* Right Column */}
        <div className="col-right">
          <div className="feed-panel">
            <div className="feed-panel__header">
              <span className="panel__title">Sentiment Headlines</span>
              <div className="feed-panel__live">
                <span className="feed-panel__live-dot" />
                Live
              </div>
            </div>
            <FeedList feed={feed} loading={sentimentLoading} />
          </div>
        </div>

      </main>
    </div>
  )
}

export default Dashboard