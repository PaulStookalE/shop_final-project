from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


# Створення форми для логіну.
class LoginForm(FlaskForm):
    # validators -- обмеження для поля. В даному випадку означає що обов'язково має бути заповненим.

    email = StringField('Email', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])

    submit = SubmitField('Log in')