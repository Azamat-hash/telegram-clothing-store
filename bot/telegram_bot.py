import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = os.environ.get('BOT_TOKEN')
WEB_APP_URL = os.environ.get('WEB_APP_URL')

if not BOT_TOKEN:
    print("ОШИБКА: BOT_TOKEN не установлен!")
    exit()

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start_command(message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("🛍️ Открыть магазин", web_app={'url': WEB_APP_URL}))
    
    bot.send_message(
        message.chat.id,
        "👋 Привет! Добро пожаловать в магазин одежды!\n\n"
        "Нажми кнопку ниже чтобы открыть каталог товаров:",
        reply_markup=keyboard
    )

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(
        message.chat.id,
        "ℹ️ Доступные команды:\n"
        "/start - начать работу\n"
        "/help - помощь\n\n"
        "Для заказа товаров используйте мини-приложение"
    )

if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling()