from . import BASE
from sqlalchemy import Column, String, Integer, Float, Text
from sqlalchemy.orm import relationship


class Item(BASE):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    category = Column(Text, nullable=False)
    image = Column(String, nullable=False)
    details = Column(Text, nullable=False)
    prcie_id = Column(String, nullable=False)

    in_cart = relationship('Cart', backref='item')
    # orders = 