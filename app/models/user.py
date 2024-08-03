from . import BASE, Cart, session
from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship



# Створення таблички користувачів.
class User(BASE):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    email = Column(String(50), nullable=False, unique=True)
    phone = Column(String(30), nullable=False, unique=True)
    password = Column(String(250), nullable=False, unique=True)
    email_confirm = Column(Boolean, nullable=True, default=False)
    admin = Column(Boolean, nullable=False, default=False)

    cart = relationship('Cart', backref='buyer')
    orders = relationship('Order', backref='customer')



    def add_to_cart(self, item_id, quantity):
        item_to_add = session.query(Cart).filter_by(item_id=item_id, quantity=quantity, vid=self.id)

        try:
            session.add(item_to_add)
            session.commit()

        except Exception as exc:
            return exc
        
        finally:
            session.close()


    def remove_from_cart(self, item_id, quantity):
        item_to_delete = session.query(Cart).filter_by(item_id=item_id, quantity=quantity, vid=self.id).first()

        try:
            session.delete(item_to_delete)
            session.commit()

        except Exception as exc:
            return exc
        
        finally:
            session.close()