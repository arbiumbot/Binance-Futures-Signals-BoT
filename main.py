from fastapi import FastAPI
import requests
import time

app = FastAPI()

TELEGRAM_TOKEN = "8384112500:AAG-QDDX-wUl0R9OS2wHsfR9znVD7SYGyVk"
CHAT_ID = "648661151"

proxies = {
    "http": "http://6MNtcfzc0O_0:cfMWDolz5RAe@p-28685.sp1.ovh:11001",
    "https": "http://6MNtcfzc0O_0:cfMWDolz5RAe@p-28685.sp1.ovh:11001"
}

def get_last_two_prices(symbol="BNBUSDT"):
    url = f"https://fapi.binance.com/fapi/v1/klines?symbol={symbol}&interval=1m&limit=2"
    try:
        response = requests.get(url, proxies=proxies, timeout=10)
        data = response.json()
        price_prev = float(data[0][4])  # Закриття попередньої свічки
        price_curr = float(data[1][4])  # Закриття поточної свічки
        return price_prev, price_curr
    except Exception as e:
        print("Помилка отримання цін:", e)
        return None, None

def send_telegram_signal(symbol, entry, take1, take2, take3, stop, direction):
    msg = (
        f"🔥 *Новий сигнал для {symbol} ({direction})*\n\n"
        f"🎯 Точка входу: `{entry}`\n"
        f"✅ Тейк профіт 1: `{take1}`\n"
        f"✅ Тейк профіт 2: `{take2}`\n"
        f"✅ Тейк профіт 3: `{take3}`\n"
        f"⛔ Стоп-лосс: `{stop}`"
    )
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "Markdown"
    }
    requests.post(url, data=data)

@app.get("/")
def root():
    return {"message": "Binance Signal Bot 🔥"}

@app.get("/signal")
def send_signal(symbol: str = "BNBUSDT"):
    prev_price, curr_price = get_last_two_prices(symbol)
    if not prev_price or not curr_price:
        return {"error": "Не вдалося отримати ціни"}

    # Визначення напрямку
    direction = "LONG" if curr_price > prev_price else "SHORT"

    if direction == "LONG":
        take1 = round(curr_price * 1.01, 4)
        take2 = round(curr_price * 1.02, 4)
        take3 = round(curr_price * 1.03, 4)
        stop = round(curr_price * 0.985, 4)
    else:
        take1 = round(curr_price * 0.99, 4)
        take2 = round(curr_price * 0.98, 4)
        take3 = round(curr_price * 0.97, 4)
        stop = round(curr_price * 1.015, 4)

    send_telegram_signal(symbol.replace("USDT", "/USDT"), curr_price, take1, take2, take3, stop, direction)

    return {
        "status": "Сигнал надіслано",
        "symbol": symbol,
        "direction": direction,
        "entry": curr_price,
        "take1": take1,
        "take2": take2,
        "take3": take3,
        "stop": stop
    }