import { useState, useEffect, useCallback } from "react"
import { signalApi, priceApi } from "../services/api"

const POLL_INTERVAL = 30000

function settle(promise) {
  return promise
    .then((res) => ({ ok: true, data: res.data }))
    .catch((err) => ({ ok: false, status: err.response?.status ?? 0 }))
}

export function useSignal() {
  const [signal, setSignal] = useState(null)
  const [signalHistory, setSignalHistory] = useState([])
  const [price, setPrice] = useState(null)
  const [priceHistory, setPriceHistory] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [lastUpdated, setLastUpdated] = useState(null)

  const fetchData = useCallback(async () => {
    try {
      setError(null)

      const [signalRes, historyRes, priceRes, priceHistoryRes] =
        await Promise.all([
          settle(signalApi.getCurrent()),
          settle(signalApi.getHistory(10)),
          settle(priceApi.getCurrent()),
          settle(priceApi.getHistory(24)),
        ])

      if (signalRes.ok)       setSignal(signalRes.data)
      if (historyRes.ok)      setSignalHistory(historyRes.data)
      if (priceRes.ok)        setPrice(priceRes.data)
      if (priceHistoryRes.ok) setPriceHistory(priceHistoryRes.data)

      setLastUpdated(new Date())

      const hardErrors = [signalRes, historyRes, priceRes, priceHistoryRes]
        .filter((r) => !r.ok && r.status !== 404)
      if (hardErrors.length > 0) {
        setError("Some data failed to load. Retrying shortly.")
      }

    } catch (err) {
      setError(err.response?.data?.detail || "Failed to fetch signal data")
    } finally {
      setLoading(false)
    }
  }, [])

  const triggerPipeline = useCallback(async () => {
    try {
      await signalApi.trigger()
      await fetchData()
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to trigger pipeline")
    }
  }, [fetchData])

  useEffect(() => {
    fetchData()
    const interval = setInterval(fetchData, POLL_INTERVAL)
    return () => clearInterval(interval)
  }, [fetchData])

  return {signal,signalHistory,price,priceHistory,loading,error,lastUpdated,refetch: fetchData,triggerPipeline,}
}