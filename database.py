from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text, ForeignKey

SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg2://postgres:postgres@localhost/postgres'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass


class Merch(Base):
    __tablename__ = "merch"

    merch_id = Column(Integer,primary_key=True,nullable=False)
    merch_name = Column(String)
    merch_cost = Column(Integer)


class UserAuth(Base):
    __tablename__ = "user_auth"
    user_id = Column(Integer,primary_key=True,nullable=False)
    user_login = Column(String)
    user_password = Column(String)

class EmployeeInfo(Base):
    __tablename__ = 'employee_info'
    employee_id = Column(Integer, ForeignKey(UserAuth.user_id),primary_key=True,nullable=False)
    employee_name = Column(String)
    coins = Column(Integer)


class CoinTransfer(Base):
    __tablename__ = 'coin_transfer'
    transfer_id = Column(Integer,primary_key=True,nullable=False)
    sender_id = Column(Integer, ForeignKey(EmployeeInfo.employee_id))
    receiver_id = Column(Integer, ForeignKey(EmployeeInfo.employee_id))
    coins_send_amount = Column(Integer)

class EmployeeInventory(Base):
    __tablename__ = 'employee_inventory'
    entry_id = Column(Integer,primary_key=True,nullable=False)
    employee_id = Column(Integer, ForeignKey(EmployeeInfo.employee_id))
    item_type = Column(Integer, ForeignKey(Merch.merch_id))
    item_quantity = Column(Integer)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()