from fastapi import FastAPI
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Дозволити CORS (може бути корисно при фронтенді)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Проксі для доступу до Binance
proxies = {
    "http": "http://6MNtcfzc0O_0:cfMWDolz5RAe@p-28685.sp1.ovh:11001",
    "https": "http://6MNtcfzc0O_0:cfMWDolz5RAe@p-28685.sp1.ovh:11001",
}

@app.get("/")
def root():
    return {"message": "Binance Futures Proxy API запущено"}

@app.get("/symbols")
def get_symbols():
    url = "https://fapi.binance.com/fapi/v1/exchangeInfo"
    try:
        response = requests.get(url, proxies=proxies, timeout=10)
        response.raise_for_status()
        data = response.json()
        symbols = [s["symbol"] for s in data["symbols"] if s.get("contractType") == "PERPETUAL"]
        return {"symbols": symbols}
    except Exception as e:
        return {
            "error": str(e),
            "details": "Помилка при отриманні даних з Binance через проксі"
        }