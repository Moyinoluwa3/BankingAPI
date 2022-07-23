from datetime import datetime
from typing import Optional,List
from unicodedata import category
from pydantic import BaseModel, EmailStr
from enum import Enum
from pydantic.types import conint

class Gender(str,Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
class UserOutput(BaseModel):
    id : int
    email : EmailStr
    account_number:  Optional[int] = None
    created_at: datetime
    class Config:
        orm_mode = True   

class UserLogin(BaseModel):
    email: EmailStr 
    password: str

class Admin(BaseModel):
    name : str
    password: str

class AdminOut(BaseModel):
    id : int
    name : str
    class Config:
        orm_mode = True
        
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id : Optional[str] = None

class details(BaseModel):
   
    reciever: int
    amount: int
class Email(BaseModel):
    email: EmailStr

class Password(BaseModel):
    password: str


class AccountIn(BaseModel):
    BVN: int
    first_name: str
    last_name: str
    age: int
    gender : Gender
    amount: int
    type: str

class AccountOut(BaseModel):
    BVN: int
    account_number: int
    first_name: str
    last_name: str
    age: int
    gender : Gender 
    amount: int
    type: str
    acccount_status: int
    owner_id: int
    class Config:
        orm_mode = True
