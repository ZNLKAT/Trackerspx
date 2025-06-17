import os, time, logging
from kucoin.client import Client
from telegram import Bot, ParseMode

# ENV variables
KU_KEY    = os.getenv("KUCOIN_KEY")
KU_SECRET = os.getenv("KUCOIN_SECRET")
KU_PASS   = os.getenv("KUCOIN_PASSPHRASE")
TG_TOKEN  = os.getenv("TG_TOKEN")
CHAT_ID   = int(os.getenv("TG_CHAT_ID"))
SYMBOL    = os.getenv("TRACK_SYMBOL", "SPX6900-USDT")
SLEEP_SEC = int(os.getenv("SLEEP_SEC", 120))
PERCENT_THR = float(os.getenv("PERCENT_THR", 0.3))

# Init clients
logging.basicConfig(level=logging.INFO)
ku = Client(api_key=KU_KEY, api_secret=KU_SECRET, passphrase=KU_PASS)
bot = Bot(token=TG_TOKEN)

def get_price():
    try:
        ticker = ku.get_ticker(SYMBOL)
        return float(ticker["price"])
    except Exception as e:
        logging.error(f"Error fetching price: {e}")
        return None

def send_message(msg):
    try:
        bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode=ParseMode.HTML)
    except Exception as e:
        logging.error(f"Telegram error: {e}")

# Start tracking
prev_price = get_price()
if prev_price:
    send_message(f"📡 SPX-Bot started @ {prev_price:.5f} USDT")

while True:
    time.sleep(SLEEP_SEC)
    current_price = get_price()
    if current_price is None:
        continue
    change = (current_price - prev_price) / prev_price * 100
    if abs(change) >= PERCENT_THR:
        icon = "🔺" if change > 0 else "🔻"
        send_message(f"{icon} <b>{SYMBOL}</b> {current_price:.5f} USDT ({change:+.2f}%)")
        prev_price = current_price
git add main.py
git commit -m "Fix: Replace German code with working Python"
git push
