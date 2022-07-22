from fastapi import  Depends,APIRouter,HTTPException,status
from sqlalchemy.orm import Session
from . import users
from .. import models, schemas,database



router = APIRouter(
    tags=['Accounts']
)

@router.post("/accounts", response_model=schemas.AccountOut)
def create_new_accounts(account:schemas.AccountIn,db : Session = Depends(database.get_db),current_user: int= Depends(users.get_current_user)):
    old_account = db.query(models.Account).filter(models.Account.BVN == account.BVN).first()
    if old_account:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail= "This type of Account exists")
    obj = db.query(models.Account).order_by(models.Account.account_number.desc()).first()
    last_number= obj.account_number
    if last_number == None:
        account_number = 1000000000 
    account_number = last_number + 1
    new_account = models.Account(account_number=account_number,owner_id=current_user.id,**account.dict())
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account



@router.post("/accounts/sendmoney")
def send_money(details:schemas.details,db :Session = Depends(database.get_db),current_user: int= Depends(users.get_current_user)):
    try:
        sender = db.query(models.User).filter(models.User.id == current_user.id).first()
        s_account = sender.account_number
        sender_account = db.query(models.Account).filter(models.Account.account_number == s_account).first()
        if details.amount > sender_account.amount:
            return {"message": "Insufficient Fundx"}
        new_amount = sender_account.amount - details.amount
        sender_account.amount = new_amount
        db.commit()
        db.refresh(sender_account)
        reciever = db.query(models.Account).filter(models.Account.account_number == details.reciever).first()
        if reciever.type != sender_account.type:
            return {"message": "IT IS not the same account"}
        new_ammount = details.amount + reciever.amount
        reciever.amount = new_ammount
        db.commit()
        db.refresh(reciever)
        return {f"You have sucessfully sent {details.amount} to {details.reciever}"}
    except Exception as err:
        return {"message" : err}