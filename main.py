import requests
import time
import logging
import os

# Налаштування логування
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Параметри
SYMBOLS = []
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
API_URL = "https://fapi.binance.com"

if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
    logging.error("TELEGRAM_TOKEN або TELEGRAM_CHAT_ID не встановлені в змінних середовища!")
    exit(1)

def get_futures_symbols():
    try:
        response = requests.get(API_URL + "/fapi/v1/exchangeInfo", timeout=10)
        response.raise_for_status()
        data = response.json()
        return [s['symbol'] for s in data['symbols'] if s['contractType'] == 'PERPETUAL' and s['quoteAsset'] == 'USDT']
    except Exception as e:
        logging.error(f"Помилка при отриманні списку символів: {e}")
        return []

def get_price(symbol):
    try:
        response = requests.get(f"{API_URL}/fapi/v1/ticker/price?symbol={symbol}", timeout=5)
        response.raise_for_status()
        return float(response.json()['price'])
    except Exception as e:
        logging.error(f"Помилка при отриманні ціни для {symbol}: {e}")
        return None

def analyze(symbol):
    try:
        candles = requests.get(f"{API_URL}/fapi/v1/klines?symbol={symbol}&interval=5m&limit=50", timeout=10).json()
        closes = [float(c[4]) for c in candles]
        if closes[-1] > closes[-2] > closes[-3]:
            return "LONG"
        elif closes[-1] < closes[-2] < closes[-3]:
            return "SHORT"
    except Exception as e:
        logging.warning(f"Помилка при аналізі {symbol}: {e}")
    return None

def send_telegram(text):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        response = requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": text})
        if response.status_code != 200:
            logging.warning(f"Не вдалося надіслати повідомлення: {response.text}")
    except Exception as e:
        logging.error(f"Помилка при надсиланні повідомлення: {e}")

def main_loop():
    global SYMBOLS
    SYMBOLS = get_futures_symbols()
    if not SYMBOLS:
        logging.warning("Не знайдено символів для торгівлі.")
        return

    logging.info(f"Починаємо перевірку {len(SYMBOLS)} символів...")
    while True:
        for symbol in SYMBOLS:
            signal = analyze(symbol)
            if signal:
                price = get_price(symbol)
                if price:
                    sl = round(price * (0.99 if signal == "LONG" else 1.01), 2)
                    tp = round(price * (1.01 if signal == "LONG" else 0.99), 2)
                    message = (
                        f"📊 Сигнал по {symbol} [{signal}]\n"
                        f"💰 Ціна входу: {price}\n"
                        f"🎯 TP: {tp}\n"
                        f"🛑 SL: {sl}"
                    )
                    send_telegram(message)
        time.sleep(10)

if __name__ == "__main__":
    main_loop()