from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Binance API напряму працює"

@app.route("/exchange-info")
def exchange_info():
    try:
        response = requests.get("https://fapi.binance.com/fapi/v1/exchangeInfo", timeout=10)
        response.raise_for_status()
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": "Помилка при отриманні даних з Binance", "details": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # ← Render встановлює PORT
    app.run(host="0.0.0.0", port=port)