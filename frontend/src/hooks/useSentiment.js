import { useState, useEffect, useCallback } from "react"
import { sentimentApi } from "../services/api"

const POLL_INTERVAL = 30000

function settle(promise) {
  return promise
    .then((res) => ({ ok: true, data: res.data }))
    .catch((err) => ({ ok: false, status: err.response?.status ?? 0 }))
}

export function useSentiment(limit = 20) {
  const [feed, setFeed] = useState([])
  const [latest, setLatest] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [lastUpdated, setLastUpdated] = useState(null)

  const fetchData = useCallback(async () => {
    try {
      setError(null)

      const [feedRes, latestRes] = await Promise.all([
        settle(sentimentApi.getFeed(limit)),
        settle(sentimentApi.getLatest()),
      ])

      if (feedRes.ok)   setFeed(feedRes.data)
      if (latestRes.ok) setLatest(latestRes.data)

      setLastUpdated(new Date())

      const hardErrors = [feedRes, latestRes].filter(
        (r) => !r.ok && r.status !== 404
      )
      if (hardErrors.length > 0) {
        setError("Failed to fetch sentiment data")
      }

    } catch (err) {
      setError(err.response?.data?.detail || "Failed to fetch sentiment data")
    } finally {
      setLoading(false)
    }
  }, [limit])

  useEffect(() => {
    fetchData()
    const interval = setInterval(fetchData, POLL_INTERVAL)
    return () => clearInterval(interval)
  }, [fetchData])

  return { feed, latest, loading, error, lastUpdated, refetch: fetchData }
}