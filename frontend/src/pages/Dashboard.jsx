import { useState, useRef } from "react"
import { useSignal } from "../hooks/useSignal"
import { useSentiment } from "../hooks/useSentiment"
import SignalBadge from "../components/SignalBadge"
import SentimentGauge from "../components/SentimentGauge"
import PriceChart from "../components/PriceChart"
import FeedList from "../components/FeedList"

function LastUpdated({ timestamp }) {
  if (!timestamp) return null
  return (
    <span className="dashboard__updated">
      Last updated {timestamp.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
    </span>
  )
}

function ErrorBanner({ message }) {
  if (!message) return null
  return <div className="dashboard__error">{message}</div>
}

function StatCard({ label, value, sub }) {
  return (
    <div className="stat-card">
      <div className="stat-card__label">{label}</div>
      <div className="stat-card__value">{value}</div>
      {sub && <div className="stat-card__sub">{sub}</div>}
    </div>
  )
}

function Dashboard() {
  const {
    signal,price,priceHistory,loading: signalLoading,error: signalError,lastUpdated,triggerPipeline,
  } = useSignal()

  const { feed, loading: sentimentLoading, error: sentimentError } = useSentiment(20)

  const [aiText, setAiText]       = useState("")
  const [aiLoading, setAiLoading] = useState(false)
  const [aiError, setAiError]     = useState("")
  const abortRef                  = useRef(null)

  const isLoading    = signalLoading || sentimentLoading
  const errorMessage = signalError || sentimentError

  async function handleExplain() {
    setAiText("")
    setAiError("")
    setAiLoading(true)

    abortRef.current = new AbortController()

    try {
      const res = await fetch(
        `${import.meta.env.VITE_API_URL || "http://localhost:8000"}/ai/explain`,
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

  function formatMarketCap(value) {
    if (!value) return "-"
    if (value >= 1e12) return "$" + (value / 1e12).toFixed(2) + "T"
    if (value >= 1e9)  return "$" + (value / 1e9).toFixed(2) + "B"
    return "$" + value.toLocaleString()
  }

  function formatVolume(value) {
    if (!value) return "-"
    if (value >= 1e9) return "$" + (value / 1e9).toFixed(2) + "B"
    if (value >= 1e6) return "$" + (value / 1e6).toFixed(2) + "M"
    return "$" + value.toLocaleString()
  }

  return (
    <div className="dashboard">

      <header className="dashboard__header">
        <div className="dashboard__title-group">
          <h1 className="dashboard__title">
            <span className="dashboard__title-btc">₿</span> SATURN
          </h1>
          <p className="dashboard__subtitle">
            AI-powered signals from {feed.length} scored headlines
          </p>
        </div>
        <div className="dashboard__controls">
          <LastUpdated timestamp={lastUpdated} />
          <button
            className="dashboard__trigger-btn"
            onClick={triggerPipeline}
            disabled={isLoading}
          >
            {isLoading ? "Running..." : "↻ Refresh Signal"}
          </button>
        </div>
      </header>

      <ErrorBanner message={errorMessage} />

      <section className="dashboard__signal-row">
        <div className="dashboard__signal-main">
          <h2 className="dashboard__section-title">Current Signal</h2>
          <SignalBadge signal={signal?.signal} confidence={signal?.confidence} />
        </div>
        <div className="dashboard__gauge">
          <h2 className="dashboard__section-title">Market Sentiment</h2>
          <SentimentGauge
            positiveCount={signal?.positive_count}
            negativeCount={signal?.negative_count}
            neutralCount={signal?.neutral_count}
            sampleSize={signal?.sample_size}
          />
        </div>
      </section>

      <section className="dashboard__stats-row">
        <StatCard
          label="BTC Price"
          value={price ? "$" + price.price_usd.toLocaleString() : "-"}
          sub={
            price
              ? (price.price_change_24h_pct >= 0 ? "+" : "") +
                price.price_change_24h_pct?.toFixed(2) + "% (24h)"
              : null
          }
        />
        <StatCard label="Market Cap"   value={formatMarketCap(price?.market_cap_usd)} />
        <StatCard label="Volume (24h)" value={formatVolume(price?.volume_24h_usd)} />
        <StatCard
          label="Avg Sentiment"
          value={
            signal?.avg_sentiment_score != null
              ? (signal.avg_sentiment_score * 100).toFixed(1) + "%"
              : "-"
          }
          sub={(signal?.sample_size ?? 0) + " articles analysed"}
        />
      </section>

      <section className="dashboard__chart-section">
        <h2 className="dashboard__section-title">Price History</h2>
        <PriceChart priceHistory={priceHistory} currentPrice={price} />
      </section>

      <section className="dashboard__feed-section">
        <h2 className="dashboard__section-title">Sentiment Feed</h2>
        <FeedList feed={feed} loading={sentimentLoading} />
      </section>

      <section className="dashboard__ai-section">
        <div className="dashboard__ai-header">
          <h2 className="dashboard__section-title">Saturn-AI Signal Analysis</h2>
          <button
            className="dashboard__ai-btn"
            onClick={aiLoading ? handleAbort : handleExplain}
            disabled={!signal}
          >
            {aiLoading ? "⏹ Stop" : "✦ Ask Saturn-AI"}
          </button>
        </div>
        {aiError && <div className="dashboard__error">{aiError}</div>}
        {(aiText || aiLoading) && (
          <div className="dashboard__ai-output">
            <p className="dashboard__ai-text">
              {aiText}
              {aiLoading && <span className="dashboard__ai-cursor" />}
            </p>
          </div>
        )}
        {!aiText && !aiLoading && !aiError && (
          <p className="dashboard__ai-placeholder">
            Click "Ask Saturn-AI" to get a comprehensive breakdown of the current signal.
          </p>
        )}
      </section>

    </div>
  )
}

export default Dashboard