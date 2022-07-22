
from sqlalchemy.sql.expression import text
from sqlalchemy import TIMESTAMP, Column,Integer, String , Boolean
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class Account(Base):
    __tablename__ = "account"
    BVN = Column(Integer,primary_key= True, nullable=False)#BVN means the bank verification number 
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    account_number= Column(Integer,nullable=False,unique=True)
    amount= Column(Integer)
    type= Column(String(3))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')) 
    
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key= True , nullable=False)
    email = Column(String, nullable=False, unique=True)
    password= Column(String, nullable=False)
    account_number = Column(Integer,ForeignKey("account.account_number", ondelete="CASCADE"))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Admin(Base):
    __tablename__= "admins"
    id = Column(Integer, primary_key= True , nullable=False)
    name = Column(String, nullable=False)
    password= Column(String, nullable=False)
