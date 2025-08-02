from flask import Flask, jsonify
import requests

app = Flask(__name__)

BINANCE_BASE_URL = "https://fapi.binance.com"

@app.route("/exchange-info")
def get_exchange_info():
    try:
        url = f"{BINANCE_BASE_URL}/fapi/v1/exchangeInfo"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": "Помилка при отриманні даних з Binance", "details": str(e)}), 500

@app.route("/")
def home():
    return "Binance API напряму працює"

if __name__ == "__main__":
    app.run(debug=True)