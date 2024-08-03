from . import BASE
from sqlalchemy import Column, Integer, ForeignKey



# Створення таблички корзини.
class Cart(BASE):
    __tablename__ = 'carts'

    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False, default=1)

    user_id = Column(ForeignKey('users.id'), nullable=False)
    item_id = Column(ForeignKey('items.id'), nullable=False)