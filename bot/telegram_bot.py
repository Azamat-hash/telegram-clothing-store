import os
import logging
import time
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self):
        self.token = os.environ.get('BOT_TOKEN')
        if not self.token:
            raise ValueError("BOT_TOKEN not set")
        
        self.bot = telebot.TeleBot(self.token)
        self.setup_handlers()
        logger.info("Bot initialized")

    def setup_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def start_command(message):
            keyboard = InlineKeyboardMarkup()
            web_app_url = os.environ.get('WEB_APP_URL', '')
            if web_app_url:
                keyboard.add(InlineKeyboardButton("🛍️ Открыть магазин", web_app={'url': f"{web_app_url}/client"}))
            
            self.bot.send_message(
                message.chat.id,
                "👕 Добро пожаловать в магазин одежды!\n\nНажмите кнопку ниже чтобы открыть магазин:",
                reply_markup=keyboard
            )

    def run_polling(self):
        logger.info("Starting bot polling...")
        while True:
            try:
                self.bot.infinity_polling()
            except Exception as e:
                logger.error(f"Polling error: {e}")
                time.sleep(10)

def run_bot():
    try:
        bot = TelegramBot()
        bot.run_polling()
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")

if __name__ == '__main__':
    run_bot()
