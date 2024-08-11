from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, FileField, SubmitField
from wtforms.validators import DataRequired, Length



# Створення форми для додавання нового товару до каталогу.
class AddNewItemForm(FlaskForm):
    name = StringField('Name: ', validators=[DataRequired(), Length(50)])
    price = FloatField('Price: ', validators=[DataRequired()])
    category = StringField('Category: ', validators=[DataRequired(), Length(50)])
    details = StringField('Details: ', validators=[DataRequired()])
    price_id = StringField('Price ID: ', validators=[DataRequired()])
    image = FileField('Image: ', validators=[DataRequired()])

    submit = SubmitField('Add Item')
    