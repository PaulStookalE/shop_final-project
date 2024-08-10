from sqlalchemy import Column, Integer, Float, Text, String
from sqlalchemy.orm import relationship
from . import BASE


class Item(BASE):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    category = Column(Text, nullable=False)
    image = Column(String, nullable=False)
    details = Column(String, nullable=False)
    price_id = Column(String, nullable=False)

    in_cart = relationship("Cart", backref="item")
    orders = relationship("Ordered_Item", backref="item")