from . import BASE
from sqlalchemy import Column, ForeignKey, String, Integer, DateTime
from sqlalchemy.orm import relationship


class Order(BASE):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    time = Column(DateTime, nullable=False)
    status = Column(String(50), nullable=False)
    
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    items = relationship('Ordered_Item', backref='order')


class OrderedItems(BASE):
    __tablename__ = 'ordered_items'
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    quantity = Column(Integer, ForeignKey('carts.quantity'), nullable=False)