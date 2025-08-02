from flask import Flask, jsonify
import requests
import random
import os

app = Flask(__name__)

# 🔐 Заміни токен і chat_id на свої
BOT_TOKEN = "8384112500:AAG-QDDX-wUl0R9OS2wHsfR9znVD7SYGyVk"
CHAT_ID = "648661151"

# 📈 Отримання поточної ціни з Binance
def get_current_price(symbol="bnbusdt"):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol.upper()}"
        response = requests.get(url)
        data = response.json()
        return float(data["price"])
    except Exception as e:
        print("Помилка отримання ціни:", e)
        return None

# 📤 Надсилання сигналу в Telegram
def send_telegram_signal(signal):
    text = (
        f"📊 Сигнал для {signal['symbol']}\n"
        f"🔹 Entry: {signal['entry']}\n"
        f"🎯 TP1: {signal['tp1']}\n"
        f"🎯 TP2: {signal['tp2']}\n"
        f"🎯 TP3: {signal['tp3']}\n"
        f"🛑 SL: {signal['sl']}"
    )
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, json=payload)

# ⚙️ Генерація сигналу на основі ціни
def generate_signal():
    current_price = get_current_price("bnbusdt")
    if not current_price:
        current_price = random.uniform(200, 300)  # fallback

    entry = round(current_price, 2)
    tp1 = round(entry * 1.01, 2)
    tp2 = round(entry * 1.02, 2)
    tp3 = round(entry * 1.03, 2)
    sl = round(entry * 0.99, 2)

    return {
        "symbol": "BNB/USDT",
        "entry": entry,
        "tp1": tp1,
        "tp2": tp2,
        "tp3": tp3,
        "sl": sl
    }

# 🌐 HTTP endpoint
@app.route('/signal/send', methods=['GET'])
def send_signal():
    signal = generate_signal()
    send_telegram_signal(signal)
    return jsonify({
        "status": "Сигнал надіслано",
        "symbol": signal["symbol"],
        "entry": signal["entry"],
        "tp1": signal["tp1"],
        "tp2": signal["tp2"],
        "tp3": signal["tp3"],
        "sl": signal["sl"]
    })

# 🔁 Тестовий root маршрут
@app.route('/')
def index():
    return 'Binance Futures Signal Bot запущено ✅'

# 🏁 Запуск
if __name__ == '__main__':
    app.run(debug=True)