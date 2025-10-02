import os
import logging
from flask import Flask, render_template, jsonify
import threading

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-123')

# Простые API маршруты без базы данных
@app.route('/')
def home():
    return render_template('client.html')

@app.route('/client')
def client():
    return render_template('client.html')

@app.route('/api/products')
def get_products():
    # Возвращаем тестовые данные вместо базы данных
    return jsonify([])

@app.route('/api/categories')
def get_categories():
    # Возвращаем тестовые категории
    return jsonify([
        {'id': 1, 'name': 'Мужская одежда'},
        {'id': 2, 'name': 'Женская одежда'},
        {'id': 3, 'name': 'Детская одежда'}
    ])

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'message': 'Server is running'})

# Запуск бота в фоновом режиме
def start_bot():
    try:
        from bot.telegram_bot import run_bot
        print("✅ Starting Telegram bot...")
        run_bot()
    except Exception as e:
        print(f"❌ Bot error: {e}")

# Запускаем бот при старте приложения
if os.environ.get('START_BOT', 'False').lower() == 'true':
    print("🟡 Initializing bot...")
    bot_thread = threading.Thread(target=start_bot, daemon=True)
    bot_thread.start()
    print("✅ Bot thread started")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
