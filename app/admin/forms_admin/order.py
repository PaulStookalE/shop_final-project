from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired



# Створення форми для додавання нового товару до каталогу.
class OrderEditForm(FlaskForm):
    status = StringField('Status: ', validators=[DataRequired()])

    submit = SubmitField('Edit Order Status')
    