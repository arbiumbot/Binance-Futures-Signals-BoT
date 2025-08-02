from flask import Flask, jsonify
import requests

app = Flask(__name__)

PROXY_API_KEY = "63f98a2c-caac-4b4b-9523-58ce5350d486"
PROXY_URL = f"https://proxy.scrapeops.io/v1/?api_key={PROXY_API_KEY}&url="

BINANCE_BASE_URL = "https://fapi.binance.com"

@app.route("/exchange-info")
def get_exchange_info():
    try:
        url = PROXY_URL + BINANCE_BASE_URL + "/fapi/v1/exchangeInfo"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": "Помилка при отриманні даних з Binance", "details": str(e)}), 500

@app.route("/")
def home():
    return "Binance API через ScrapeOps Proxy працює"

if __name__ == "__main__":
    app.run(debug=True)