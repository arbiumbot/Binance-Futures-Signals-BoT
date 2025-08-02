from fastapi import FastAPI
import requests
import random
import time

app = FastAPI()

TELEGRAM_TOKEN = "8384112500:AAG-QDDX-wUl0R9OS2wHsfR9znVD7SYGyVk"
TELEGRAM_CHAT_ID = "648661151"

# Тестовий список валют
symbols = ["BTC/USDT", "ETH/USDT", "BNB/USDT"]

def send_telegram_signal(symbol, entry, tp1, tp2, tp3, sl, position="LONG"):
    message = f"""🔔 Сигнал на ф'ючерси Binance 🔔
Пара: {symbol}
Позиція: {position}
Точка входу: {entry}
Take Profit 1: {tp1}
Take Profit 2: {tp2}
Take Profit 3: {tp3}
Stop Loss: {sl}"""
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=payload)
    return response.json()


@app.get("/")
def root():
    return {"message": "Binance Futures Signal Bot запущено"}


@app.get("/send-test-signal")
def send_signal():
    symbol = random.choice(symbols)
    entry = round(random.uniform(25000, 30000), 2)
    tp1 = round(entry * 1.01, 2)
    tp2 = round(entry * 1.02, 2)
    tp3 = round(entry * 1.03, 2)
    sl = round(entry * 0.99, 2)
    
    send_telegram_signal(symbol, entry, tp1, tp2, tp3, sl)
    return {"status": "Сигнал надіслано", "symbol": symbol}