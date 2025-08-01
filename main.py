import requests
import time
import hmac
import hashlib
import logging
import os

# Параметри
SYMBOLS = []
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
API_URL = "https://fapi.binance.com"

def get_futures_symbols():
    response = requests.get(API_URL + "/fapi/v1/exchangeInfo")
    data = response.json()
    return [s['symbol'] for s in data['symbols'] if s['contractType'] == 'PERPETUAL' and s['quoteAsset'] == 'USDT']

def get_price(symbol):
    response = requests.get(f"{API_URL}/fapi/v1/ticker/price?symbol={symbol}")
    return float(response.json()['price'])

def analyze(symbol):
    candles = requests.get(f"{API_URL}/fapi/v1/klines?symbol={symbol}&interval=5m&limit=50").json()
    closes = [float(c[4]) for c in candles]
    if closes[-1] > closes[-2] and closes[-2] > closes[-3]:
        return "LONG"
    elif closes[-1] < closes[-2] and closes[-2] < closes[-3]:
        return "SHORT"
    return None

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": text})

def main_loop():
    global SYMBOLS
    SYMBOLS = get_futures_symbols()
    while True:
        for symbol in SYMBOLS:
            signal = analyze(symbol)
            if signal:
                price = get_price(symbol)
                sl = round(price * (0.99 if signal == "LONG" else 1.01), 2)
                tp = round(price * (1.01 if signal == "LONG" else 0.99), 2)
                send_telegram(
                    f"Сигнал по {symbol} [{signal}]\n"
                    f"Ціна входу: {price}\n"
                    f"TP: {tp}\n"
                    f"SL: {sl}"
                )
            time.sleep(1)

if __name__ == "__main__":
    main_loop()
