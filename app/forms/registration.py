from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
# Email -- обмеження на поле, яке вимагає щоб дані були у форматі електронної пошти. Lenght -- обмеження довжини поля. EqualTo -- Обмеження для перевірки рівності чогось чомусь.
from wtforms.validators import DataRequired, Email, Length, EqualTo


# Створення форми для реєстрації.
class RegisterForm(FlaskForm):

    name = StringField('Name', validators=[DataRequired(), Length(max=50)])
    Phone = StringField('Phone Number', validators=[DataRequired(), Length(max=30)])
    email = StringField('Email', validators=[DataRequired(), Email])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo(
        'password',
        message='Password must be match',
    )])

    submit = SubmitField('Register')