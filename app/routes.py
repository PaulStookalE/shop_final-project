from . import app, login_manager
from .models import User, session, Item
from flask import redirect, render_template, url_for, flash
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash


# Залогінення користувача.
@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(id=user_id)


# Створення головної сторінки із товарами.
@app.route('/')
def home():
    items = session.query(Item).all()
    return render_template('home.html', items=items)


# Створення сторінки логіну.
@app.route('/login', methods=['GET', 'POST'])
def log_in():

    # Перевірка чи є користувач залогінений.
    if current_user.is_authentificated:
        return redirect(url_for('home'))
    
    else:
        form = LoginForm()
        
        # Перевірка на те чи правильно заповнені поля форми.
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
                return redirect(url_for(log_in))
            
        else:
            return render_template('login.html', form=form)
        


# Створення стоірнки для реєстрації.
@app.route('/register', method=['POST', 'GET'])
def registration():

    # Перевірка чи користувач зареєстрований, і якщо так -- його перекидує на головну сторінку.
    if current_user.is_authentificated:
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