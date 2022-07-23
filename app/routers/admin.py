from fastapi import HTTPException, status, Depends,APIRouter,Response
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from typing import List
from . import users
from .. import auth
from .. import models, schemas, utils
from ..database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='admin/login')
router = APIRouter(tags=['Admins'])

auth_handler = auth.Auth()

def get_current_admin(token: str = Depends(oauth2_scheme),db : Session = Depends(get_db)):

    token_data = auth_handler.decode_token(token)
   
    admin = db.query(models.Admin).filter(models.Admin.id ==token_data).first()
    return admin

@router.post("/admin", response_model=schemas.AdminOut)
def create_admin(admin:schemas.Admin,db: Session = Depends(get_db)):
    admin = db.query(models.Admin).filter(models.Admin.name == admin.name).first()
    admin = jsonable_encoder(admin)
    if admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail= "Admin exists")
    try:
        hashed_password = utils.hash(admin.password)
        admin.password = hashed_password
        new_admin= models.Admin(**admin.dict())
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
        return new_admin
    except Exception as err:
        return {"message" : err}

@router.get('/admin/all',response_model=List[schemas.AdminOut])
def get_admin(db: Session = Depends(get_db),current_user: int= Depends(users.get_current_user)):
    admins = db.query(models.Admin).all()
    return admins

@router.post('/admin/login', response_model=schemas.Token)
def login(admin_credentials: OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):
    
    admin = db.query(models.Admin).filter(models.Admin.name == admin_credentials.username).first()
    print (admin)
    
    
    if not admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"invalid credentials")

    if not utils.verify(admin_credentials.password, admin.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"invalid credentials")
   
    access_token = auth_handler.encode_token(admin.id)

    return {"access_token": access_token, "token_type": "bearer"}

@router.get('/admin/{id}' ,response_model=schemas.AdminOut)
def get_an_admin(id:int,db : Session = Depends(get_db),current_user: int= Depends(users.get_current_user)):
    admin = db.query(models.Admin).filter(models.Admin.id == id).first()

    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="admin does not exist")

    return admin


@router.get("/admin/accounts/all", response_model=List[schemas.AccountOut])
def get_all_accounts(db : Session = Depends(get_db), limit:int =10,current_admin: int= Depends(get_current_admin)):
    accounts = db.query(models.Account).limit(limit).all()
    return accounts

@router.get("/admin/accounts/{id}", response_model=schemas.AccountOut)
def get_an_account(id:int,db : Session = Depends(get_db), current_admin: int= Depends(get_current_admin)):
    account = db.query(models.Account).filter(models.Account.owner_id == id).first()
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="account does not exist")
    return account

@router.delete("/admin/delete/{id}", status_code=204)
def delete_an_account(id:int,db :Session= Depends(get_db),current_admin:int = Depends(get_current_admin)):
    account= db.query(models.Account).filter(models.Account.owner_id == id)
    if account.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")

    account.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/admin/users/all",response_model=List[schemas.UserOutput])
def get_all_users(db : Session = Depends(get_db),current_admin:int = Depends(get_current_admin)):
    users = db.query(models.User).all()
    return users


@router.get('/admin/users/{id}',response_model=schemas.UserOutput)
def Get_user(id: int,db : Session = Depends(get_db),current_admin:int = Depends(get_current_admin)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user does not exist")

    return user

@router.post("/admin/freeze/{id}")
def Freeze_account(id: int,db : Session = Depends(get_db),current_admin:int = Depends(get_current_admin)):
    account= db.query(models.Account).filter(models.Account.owner_id == id)
    account_object = account.first()
    if account_object == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    account_object.acccount_status = 3
    db.commit()
    db.refresh(account_object)
    return {"message":"Account has been Freezed"}


@router.post("/admin/inactive/{id}")
def Freeze_account(id: int,db : Session = Depends(get_db),current_admin:int = Depends(get_current_admin)):
    account= db.query(models.Account).filter(models.Account.owner_id == id)
    account_object = account.first()
    if account_object == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    account_object.acccount_status = 2
    db.commit()
    db.refresh(account_object)
    return {"message":"Account has been made Inactive"}