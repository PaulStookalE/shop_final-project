from flask import Blueprint, flash, redirect, render_template, url_for
from ..models import Order, session, Item
from utils import admin_only
from .forms_admin import AddNewItemForm, OrderEditForm


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



# Створення роуту для з формою для додання нового товару до каталогу.
@admin.route('/add_item', methods=['POST', 'GET'])
@admin_only
def add_item():
    form = AddNewItemForm()

    if form.validate_on_submit():
        
        name = form.name.data
        price = form.price.data
        category = form.category.data
        details = form.details.data
        price_id = form.price_id.data
        image = url_for('static', filename=f'uploads/{form.image.data.filename}')

        item = Item(
            name=name,
            price=price,
            category=category,
            details=details,
            price_id=price_id,
            image=image
        )

        try:
            session.add(item)
            session.commit()
            flash(f'{name} added successfully', 'success')
            return redirect(url_for(admin.items))
        
        except Exception as exc:
            raise exc
        
        finally:
            session.close()

    else:
        return render_template('admin/add_item.html')



@admin.route('/edit/<string:type>/<int:id>', methods=['GET', 'POST'])
@admin_only
def edit(type, id):

    # Cтворення роуту для редагування товару.
    if type == 'item':
        item = session.query(Item).get(id)

        form = AddNewItemForm(
            name=item.name,
            price=item.price,
            category=item.category,
            details=item.details,
            price_id=item.price_id,
            image=item.image
        )

        if form.validate_on_submit:
            item.name = form.name.data
            item.price = form.price.data
            item.category = form.category.data
            item.details = form.details.data
            item.price_id = form.price_id.data
            item.image = url_for('static', filename=f'uploads/{form.image.data.filename}')
                                
        try:
            session.commit()
            return redirect(url_for('admin.items'))
        
        except Exception as exc:
            raise exc
        
        finally:
            session.close()


    # Створення роуту для редагування замовлення (статусу замовлення)
    elif type == 'order':
        order = session.query(Order).get(id)

        form = OrderEditForm(
            status = order.status
        )

        if form.validate_on_submit:
            order.status = form.status.data

            try:
                session.commit()
                return redirect(url_for('admin.admin_home'))
        
            except Exception as exc:
                raise exc
        
            finally:
                session.close()

    else:
        return render_template('admin/add_item.html', form=form)
    


# Створення роуту для видалення товару із каталогу. 
@admin.route('/delete_item/<int:id>')
@admin_only
def delete_item(id):
    item_to_delete = session.query(Item).get(all)

    session.delete(item_to_delete)
    session.commit()
    session.close()

    flash(f'{item_to_delete} was deleted successfully', 'success')

    return redirect(url_for('admin.items'))