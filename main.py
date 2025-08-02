import requests
from flask import Flask, jsonify
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ⚠️ HTTP-проксі (робочий на момент написання)
PROXY = {
    "http": "http://51.159.115.233:3128",
    "https": "http://51.159.115.233:3128",
}

@app.route("/")
def index():
    return "Binance API через проксі працює!"

@app.route("/symbols")
def symbols():
    url = "https://fapi.binance.com/fapi/v1/exchangeInfo"
    try:
        response = requests.get(url, proxies=PROXY, timeout=10)
        response.raise_for_status()
        data = response.json()
        symbols = [s['symbol'] for s in data['symbols'] if s['contractType'] == 'PERPETUAL']
        logging.info(f"Знайдено {len(symbols)} символів.")
        return jsonify(symbols)
    except requests.exceptions.RequestException as e:
        logging.error(f"Помилка при запиті: {e}")
        return jsonify({"error": "Помилка при отриманні даних з Binance"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)