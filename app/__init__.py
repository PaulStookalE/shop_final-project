from datetime import datetime
from flask import Flask
from flask_login import LoginManager
from dotenv import load_dotenv
import os
from .models import create_db, User, Cart, Item, Order, OrderedItems


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_TRACKMODIFICATION'] = os.getenv('STM')

login_manager = LoginManager()
login_manager.init_app(app)

create_db()


# Створення контекстного процесора, який передаватиме у HTML щось, у даному випадку час.
@app.context_processor
def inject():
    return {'now': datetime.utcnow()}