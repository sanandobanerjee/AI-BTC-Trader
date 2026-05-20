import {
  LineChart, Line, XAxis, YAxis,
  CartesianGrid, Tooltip, ResponsiveContainer
} from "recharts"

function formatTime(isoString) {
  if (!isoString) return ""
  return new Date(isoString).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
}

function formatPrice(value) {
  return "$" + Number(value).toLocaleString()
}

function formatMarketCap(v) {
  if (!v) return "-"
  if (v >= 1e12) return "$" + (v / 1e12).toFixed(2) + "T"
  if (v >= 1e9)  return "$" + (v / 1e9).toFixed(2) + "B"
  return "$" + v.toLocaleString()
}

function PriceChart({ priceHistory, currentPrice }) {
  if (!priceHistory || priceHistory.length === 0) {
    return <div className="price-chart price-chart--empty"><p>No price history yet</p></div>
  }

  const chartData = [...priceHistory].reverse().map((s) => ({
    time:  formatTime(s.created_at),
    price: s.price_usd,
  }))

  const prices   = chartData.map((d) => d.price)
  const minPrice = Math.min(...prices)
  const maxPrice = Math.max(...prices)
  const padding  = (maxPrice - minPrice) * 0.1
  const yDomain  = [Math.floor(minPrice - padding), Math.ceil(maxPrice + padding)]

  const changePositive = (currentPrice?.price_change_24h_pct ?? 0) >= 0

  return (
    <div className="price-chart">
      {currentPrice && (
        <div className="price-chart__current">
          <div className="price-chart__stat">
            <span className="price-chart__stat-label">Price - </span>
            <span className="price-chart__stat-value">
              {formatPrice(currentPrice.price_usd)}
            </span>
          </div>
          <div className="price-chart__divider" />
          <div className="price-chart__stat">
            <span className="price-chart__stat-label">24h Change </span>
            <span className={`price-chart__stat-value price-chart__stat-value--${changePositive ? "positive" : "negative"}`}>
              {changePositive ? "+" : ""}{currentPrice.price_change_24h_pct?.toFixed(2)}%
            </span>
          </div>
          <div className="price-chart__divider" />
          <div className="price-chart__stat">
            <span className="price-chart__stat-label">Market Cap - </span>
            <span className="price-chart__stat-value">
              {formatMarketCap(currentPrice.market_cap_usd)}
            </span>
          </div>
        </div>
      )}
      <div className="price-chart__graph">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData} margin={{ top: 8, right: 10, left: -20, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#2a2a2a" vertical={false} />
            <XAxis
              dataKey="time"
              tick={{ fontSize: 10, fill: "#808080", fontFamily: "JetBrains Mono" }}
              interval="preserveStartEnd"
              axisLine={false}
              tickLine={false}
            />
            <YAxis
              domain={yDomain}
              tickFormatter={formatPrice}
              tick={{ fontSize: 10, fill: "#808080", fontFamily: "JetBrains Mono" }}
              width={72}
              axisLine={false}
              tickLine={false}
            />
            <Tooltip
              formatter={(value) => [formatPrice(value), "BTC"]}
              contentStyle={{
                background: "#2a2a2a",
                border: "1px solid #4d4d4d",
                borderRadius: 6,
                fontSize: 12,
                fontFamily: "JetBrains Mono",
              }}
              labelStyle={{ color: "#808080" }}
              itemStyle={{ color: "#f7931a" }}
            />
            <Line
              type="monotone"
              dataKey="price"
              stroke="#f7931a"
              strokeWidth={1.5}
              dot={false}
              activeDot={{ r: 3, fill: "#f7931a" }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}

export default PriceChart