import axios from "axios"

const api=axios.create({
    baseURL:import.meta.env.VITE_API_URL || "http://localhost:8000",
    timeout:60000,
    headers:{
        "Content-Type":"application/json",
    },
})

api.interceptors.response.use(
    (response)=>response,
    (error)=>{
        const status = error.response?.status
        const details=error.response?.data?.detail || error.message
        console.error(`API Error [${status}]: ${details}`)
        return Promise.reject(error)
    }
)

export const sentimentApi={
    getLatest: ()=> api.get("/sentiment/latest"),
    getFeed:(limit=20)=> api.get("/sentiment/feed",{params:{limit}}),
    getFeedBySource:(source,limit=20)=>
        api.get(`/sentiment/feed/${source}`,{params:{limit}}),
}

export const signalApi={
    getCurrent:()=>api.get("/signals/current"),
    getHistory: (limit = 20) => api.get("/signals/history", { params: { limit } }),
    trigger: () => api.post("/signals/trigger")
}

export const priceApi = {
  getCurrent: () => api.get("/price/btc"),
  getHistory: (limit = 24) =>
    api.get("/price/btc/history", { params: { limit } }),
}

export default api