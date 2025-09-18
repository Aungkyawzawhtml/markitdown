import requests
import logging
import os
from datetime import datetime, timedelta
import time

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get configuration from environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID', "-1002265978051"))
API_URL = "https://api.thaistock2d.com/live"

def send_telegram_message(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": CHANNEL_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        response = requests.post(url, data=data, timeout=10)
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Telegram error: {e}")
        return False

def fetch_stock_data():
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(API_URL, headers=headers, timeout=15)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        logger.error(f"API error: {e}")
        return None

def main():
    logger.info("🤖 Bot starting...")
    
    # Test message
    send_telegram_message("🚀 Bot started on Railway!")
    
    while True:
        try:
            current_time = datetime.utcnow() + timedelta(hours=6, minutes=30)
            current_hour_min = current_time.strftime("%H:%M")
            
            if current_hour_min in ["12:01", "16:30"]:
                data = fetch_stock_data()
                if data:
                    # Process and send data here
                    send_telegram_message("📊 Data received successfully!")
                    
            time.sleep(60)
            
        except Exception as e:
            logger.error(f"Error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
