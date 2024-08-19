from datetime import datetime
from flask import Flask
from flask_login import LoginManager
from dotenv import load_dotenv
import os
from flask_bootstrap import Bootstrap

from .models import create_db, Cart, Item, Order, Ordered_Item, User
from app.models.base import create_db

from .admin.routes import admin
from .utils import send_confirmation_mail, mail

load_dotenv()

app = Flask(__name__)
app.register_blueprint(admin)           # З'єднання адміна з апкою.
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
# Не записуватиме будь яку зміну в БД як важливі зміну.
app.config['SQLALCHEMY_TRACKMODIFICATION'] = os.getenv('STM')


# 
app.config['MAIL_USERNAME'] = os.getenv('EMAIL')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_TLS')


# Ініціалізація класу Bootstrap для подальшого його використання у HTML.
Bootstrap(app)
mail.init_app(app)

# Ініціалізація менеджера логінів.
login_manager = LoginManager()
login_manager.init_app(app)


# Створення БД.
create_db()


# Створення контекстного процесора, який передаватиме у HTML щось, у даному випадку час.
@app.context_processor
def inject():
    return {'now': datetime.utcnow()}


# Підключення до основної програми роутів для звичайного користувача та для адміна.
from . import routes
from .admin import routes


