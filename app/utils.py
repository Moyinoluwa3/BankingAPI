from passlib.context import CryptContext
from fastapi import APIRouter,Request
from fastapi import Depends
from sqlalchemy.orm import Session
from .database import get_db
from . import models,schemas,utils
from . import auth
auth_handler = auth.Auth()



from fastapi_mail import FastMail,MessageSchema,ConnectionConfig
router =APIRouter(
    tags=["Forgot"]
)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


conf = ConnectionConfig(
    MAIL_USERNAME="moyogundare@gmail.com",
    MAIL_FROM ="moyogundare@gmail.com",
    MAIL_PASSWORD="mkgsrzxyelttowbm",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_TLS= True,
    MAIL_SSL = False

)
#hcszkytetemklxgm
@router.post("/forgotpassword")
async def send_mail(email:schemas.Email, db: Session = Depends(get_db)):
    email =  db.query(models.User).filter(models.User.email == email.email).first()
    print(email)
    if email:
        token = auth_handler.encode_token(str(email.id))

    
    template = f"""
    <p> Dear, User </p>

   To reset your password
   <a href = "http://localhost:8000/changepassword/?token={token}">
      click here

    </a>



<p> Sincerely </p>

<p> Movie Support Team </p>

        """
 
    message = MessageSchema(
        subject="Reset Your Password",
        recipients=[email.email],  # List of recipients, as many as you can pass
        body=template,
        subtype="html"
        )
 
    fm = FastMail(conf)
    await fm.send_message(message=message)
    return {"message": "email has been sent"}

    

@router.post("/changepassword")
def changepassword(request:Request,password:schemas.Password, db: Session = Depends(get_db)):
    print(request.url)
    token = request.query_params.get("token")

    user_id = auth_handler.decode_token(token)
    print(user_id)
    
    hashed_password = utils.hash(password.password)
    new_password = hashed_password

    #cursor.execute(""" UPDATE user set password = %s where id = %s returning *""",(new_password , str(id)))
    user = db.query(models.User).filter(models.User.id == user_id).first()
    user.password = new_password
    db.commit()
    db.refresh(user)
    return {"status":"Password has been Updated"}

