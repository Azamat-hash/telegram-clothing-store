import os
import logging
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///shop.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-123')

db = SQLAlchemy(app)

# Модели базы данных
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(500))
    category = db.Column(db.String(100))
    brand = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

# Инициализация базы данных
def init_db():
    with app.app_context():
        db.create_all()
        
        # Добавляем начальные категории
        if Category.query.count() == 0:
            categories = ['Мужская одежда', 'Женская одежда', 'Детская одежда']
            for cat_name in categories:
                db.session.add(Category(name=cat_name))
            db.session.commit()
            logger.info("Initial categories added")

# API маршруты
@app.route('/')
def home():
    return render_template('client.html')

@app.route('/client')
def client():
    return render_template('client.html')

@app.route('/api/products')
def get_products():
    try:
        category = request.args.get('category')
        brand = request.args.get('brand')
        
        query = Product.query.filter_by(is_active=True)
        
        if category:
            query = query.filter(Product.category == category)
        if brand:
            query = query.filter(Product.brand == brand)
        
        products = query.all()
        return jsonify([{
            'id': p.id,
            'name': p.name,
            'description': p.description,
            'price': p.price,
            'image_url': p.image_url,
            'category': p.category,
            'brand': p.brand
        } for p in products])
    except Exception as e:
        logger.error(f"Error getting products: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/categories')
def get_categories():
    try:
        categories = Category.query.all()
        return jsonify([{'id': c.id, 'name': c.name} for c in categories])
    except Exception as e:
        logger.error(f"Error getting categories: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'message': 'Server is running'})

# Запуск бота в фоновом режиме, если переменная окружения установлена
if os.environ.get('START_BOT', 'False').lower() == 'true':
    print("🟡 Attempting to start bot...")
    try:
        from bot.telegram_bot import run_bot
        print("🟡 Bot module imported successfully")
        
        def run_bot_wrapper():
            try:
                print("🟡 Starting bot in thread...")
                run_bot()
            except Exception as e:
                print(f"🔴 Error in bot thread: {e}")
        
        import threading
        bot_thread = threading.Thread(target=run_bot_wrapper, daemon=True)
        bot_thread.start()
        print("✅ Telegram bot started in background thread")
        
    except Exception as e:
        print(f"🔴 Failed to start bot: {e}")

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
