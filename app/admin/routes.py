from flask import Blueprint, render_template
from ..models import Order, session, Item
from utils import admin_only


admin = Blueprint(
    'admin', 
    __name__,
    url_prefix='/admin',
    static_folder='static',
    template_folder='templates'
)


# Створення сторінки до якої матиме доступ лише адмін і зможе переглядати всі замовлення на сайті.
@admin.route('/')
@admin_only
def admin_home():
    orders = session.query(Order).all()
    return render_template('admin/admin.html', orders=orders)


# Створення сторінки для адмінів для перегляду всіх товарів.
@admin.route('/items')
@admin_only
def items():
    items = session.query(Item).all()
    return render_template('admin/items.html', items=items)