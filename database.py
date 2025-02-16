from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text, ForeignKey

# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Bright#1270@localhost/fastapi'
SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg2://postgres:197421@localhost/postgres'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()
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
    
    # __table__ = Table('user_auth', Base.metadata, autoload_with=engine)

class EmployeeInfo(Base):
    # __table__ = Table('employee_info', Base.metadata, autoload=True, autoload_with=engine)
    # __table__ = Table('employee_info', Base.metadata, autoload_with=engine)
    __tablename__ = 'employee_info'
    employee_id = Column(Integer, ForeignKey(UserAuth.user_id),primary_key=True,nullable=False)
    employee_name = Column(String)
    coins = Column(Integer)
    # auth_id = Column(Integer, ForeignKey(UserAuth.user_id))


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







# def result_dict(r):
#     return dict(zip(r.keys(), r))

# def result_dicts(rs): 
#     return list(map(result_dict, rs))


# get_db()
# with Session(engine) as session:
#     # statement = select(EmployeeInfo)
#     # statement = select(Merch)

#     # # list of ``User`` objects
#     # user_obj = session.scalars(statement).all()

#     # # query for individual columns
#     # statement = select(User.name, User.fullname)

#     # list of Row objects
#     # rows = session.execute(statement).all()

#     q = session.query(Merch).all()




# db = SessionLocal()
# # # q = db.query(Merch).filter(Merch.merch_cost > 100)
# q = db.query(UserAuth).filter(UserAuth.user_login == 'Ivan')
# if q.count() > 0:
#     for row in q:
#         # print(row.merch_id, row.merch_name, row.merch_cost)
#         print(row.user_id, row.user_login, row.user_password)
# else:
#     print("q is empty")

# new_employee_info = EmployeeInfo(employee_id=7, employee_name='Ivan', coins=1000)
# db.add(new_employee_info) 
# db.commit()