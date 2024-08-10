from sqlalchemy import Column, Integer, ForeignKey
from . import BASE


class Cart(BASE):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey("users.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
