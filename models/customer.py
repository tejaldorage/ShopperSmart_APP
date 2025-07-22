from sqlalchemy import Column, Integer, String
from database import Base

class Customer(Base):
    __tablename__ = 'customers'

    customer_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone_no = Column(String(20))
    location = Column(String(100))
