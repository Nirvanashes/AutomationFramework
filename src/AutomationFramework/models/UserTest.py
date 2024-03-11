from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
Base = declarative_base()
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key = True)
    name = Column(String)
    age = Column(Integer)
    email = Column(String)


class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key = True)
    name = Column(String)
    age = Column(Integer)
    email = Column(String)