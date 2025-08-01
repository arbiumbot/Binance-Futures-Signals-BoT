import requests
import logging
from flask import Flask, jsonify

app = Flask(__name__)

# Налаштування логів
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BINANCE_PROXY_BASE_URL = "https://api.binanceproxy.io"

def get_symbols():
    url = f"{BINANCE_PROXY_BASE_URL}/fapi/v1/exchangeInfo"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        symbols = [s['symbol'] for s in data['symbols'] if s['contractType'] == 'PERPETUAL']
        if not symbols:
            logging.warning("Не знайдено символів для торгівлі.")
        return symbols
    except requests.RequestException as e:
        logging.error(f"Помилка при отриманні списку символів: {e}")
        return []

@app.route("/")
def index():
    return "Binance Proxy Signal Service Active!"

@app.route("/symbols")
def symbols():
    result = get_symbols()
    return jsonify(result)

if __name__ == "__main__":
    symbols = get_symbols()
    if not symbols:
        logging.warning("Список символів порожній. Завершення програми.")
        exit(1)
    app.run(host="0.0.0.0", port=10000)