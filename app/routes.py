from itsdangerous import URLSafeTimedSerializer
from . import app, login_manager, send_confirmation_mail
from .models import User, session, Item
from flask import redirect, render_template, url_for, flash, request
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import LoginForm, RegisterForm

# Залогінення користувача.
@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(user_id)


# Створення головної сторінки із товарами.
@app.route('/')
def home():
    items = session.query(Item).all()
    return render_template('home.html', items=items)


# Створення сторінки логіну.
@app.route('/login', methods=['GET', 'POST'])
def log_in():

    # Перевірка чи є користувач залогінений.
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    else:
        form = LoginForm()
        
        # Перевірка на те чи була надіслана форма.
        if form.validate_on_submit():
            email = form.email.data
            user = session.query(User).filter_by(email=email).first()

            # Якщо користувача не існує в БД, то йому про це повідомляється і форма очищується.
            if not user:
                flash(f"User with email {email} does not exist.<br> <a href={url_for('register')}>Register</a>", "error")
                return redirect(url_for('log_in'))
    
            # Якщо все добре -- корсистувача логінить.
            elif check_password_hash(user.password, form.password.data):
                login_user(user=user)
                return redirect(url_for('home'))
        
            # Якщо користувач існує, проте пароль неправильний -- поля форми очищаються.
            else:
                flash('Password or email is incorrect', 'error')
                return redirect(url_for('log_in'))
            
        else:
            return render_template('login.html', form=form)
        


# Створення стоірнки для реєстрації.
@app.route('/register', methods=['POST', 'GET'])
def registration():

    # Перевірка чи користувач зареєстрований, і якщо так -- його перекидує на головну сторінку.
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    else:
        form = RegisterForm()

        # Перевірка чи заповнена форма правильно.
        if form.validate_on_submit():
            email = form.email.data
            user = session.query(User).filter_by(email=email).first()

            # Перевірка чи є користувач зареєстрований, і якщо ні:
            if user:
                flash(f"User with email {email} does exist.<br> <a href={url_for('log_in')}>Log in</a>", "error")
                return redirect(url_for('registration'))
            
            # Створення нового користувача.
            new_user = User(
                name = form.name.data,
                email = email,
                password = generate_password_hash(form.password.data),
                phone = form.phone.data 
            )

            # Додання користувача до БД і закриття сесії.
            try:
                session.add(new_user)
                session.commit()
                flash('Thanks for registration! You can log in now!', 'sucess')

                return redirect(url_for("log_in"))
            
            except Exception as exc:
                raise exc
            
            finally:
                session.close()
        else:
            return render_template("register.html", form=form)



# Створення сторінки для виходу з акаунта.
@app.route('/log_out')
@login_required
def log_out():
    logout_user()
    return redirect(url_for('log_in'))



# Створення роуту для додавання товару до корзини.
@app.route('/add_to_cart/<id>', methods=['POST'])
def add_to_cart(id):

    if not current_user.is_authentificated:
        flash('You must log in')
        return redirect(url_for(home))
    
    else:
        item = session.query(Item).get(id=id)

        if request.method == 'POST':
            quantity = request.form['quantity']

            current_user.add_to_cart(id, quantity)
            flash(f'''{item.name} successfully added to the <a href=cart>cart</a>.<br> <a href={url_for("cart")}>view cart!</a>''','success')
            return redirect(url_for('home'))
        


# Створення роуту для перегляду всіх замовлень користувача. Лише для залогінених
@app.route('/orders')
@login_required
def orders():
    return render_template('orders.html', orders=current_user.orders)



# Створення роуту для перегляду кошика. Лише для залогінених.
@app.route('/cart')
@login_required
def cart():
    price = 0
    quantity = []
    items = []
    price_ids = []

    for cart in current_user.cart:
        items.append(cart.item)
        quantity.append(cart.quantity)

        price_id_dict = {
            'price': cart.item.price_id,
            'quantity': cart.quantity,
        }
        price_ids.append(price_id_dict)
        price += cart.item.price * cart.quantity

    return render_template('cart.html', items=items, quantity=quantity, price_ids=price_ids, price=price)



# Створення роуту для видалення товару і його кількості із кошику.
@app.route('/remove/<id>/quantity')
@login_required
def remove(id, quantity):
    current_user.remove_from_cart(id, quantity)
    return redirect(url_for('cart'))



# Створення роуту для перегляду конкретного товару.
@app.route('/item/<int:id>')
def item(id):
    item = session.query(Item).get(id=id)
    return render_template('item.html', item=item)



# Створення роуту для виконання пошуку серед товарів.
@app.route('/search')
def search():
    query = request.args['query']
    # Дозволяє здійснювати пошук, підставляючи ключове слово в початок / середину / кінець і таким чином шукаючи
    search = f'%{query}%'

    items = session.query(Item).filter(item.name.like(search)).all()

    return render_template('home.html', items=items, search=True, query=query)



# Створення роуту для підтвердження імейлу користувача.
@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        email = serializer.loads(token, salt='email-confirmation-salt', max_age=3600)

    except:
        flash('The confirmation link is invalid', 'error')
        return redirect(url_for('log_in'))
    

    user = session.query(User).filter_by(email=email).first()
    if user.email_confirmed:
        flash('Account already confirmed. Please login', 'success')
    else: 
        user.email_confirmed = True

        try:
            session.add(User)
            session.commit()
            flash('Email adress successfully confirmed', 'success')

        except Exception as exc:
            raise exc
        
        finally:
            session.close()

            return redirect(url_for('log_in'))
        


# Створення роуту для перенадсилання імейлу
@app.route('/resend')
@login_required
def resend():
    send_confirmation_mail(current_user.email)
    logout_user()
    flash('The confirmation email was sent successfully', 'success')
    return redirect(url_for('log_in'))



# Створення роуту для підтвердження оплати.
@app.route("/success")
def payment_success():
    return render_template("payment_success.html")


# Створення роуту для відхилення оплати.
@app.route("/failure")
def payment_failure():
    return render_template("payment_failure.html")