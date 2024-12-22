import sys
import os

# Устанавливаем кодировку для корректной работы с кириллицей
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Настройка кодировки для всего приложения
os.environ['PYTHONIOENCODING'] = 'utf-8'

db = SQLAlchemy()

def create_app(config_class=Config):
    # Создаем приложение с поддержкой кириллицы
    from app.routes import app as routes_app
    
    routes_app.config['JSON_AS_ASCII'] = False
    routes_app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    
    routes_app.config.from_object(config_class)

    # Инициализируем базу данных только один раз
    if not hasattr(routes_app, 'extensions') or 'sqlalchemy' not in routes_app.extensions:
        db.init_app(routes_app)

    with routes_app.app_context():
        from . import models
        db.create_all()

    return routes_app

app = create_app()
