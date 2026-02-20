from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from datetime import date
import random
from .security import Security
from pydantic import BaseModel
from . import auth
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

SECRET_KEY = "b6c992167637afd8d25b8ceea99fb423b002429320a2d792ea58938ce1521670"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class AuthRegister(BaseModel):
    password: str
    email: str

class AuthLogin(BaseModel):
    password: str
    email: str

class Token(BaseModel):
    jwt: str | None = None

class User(BaseModel):
    email: str
    password: str
    isOnline: bool = False 

app = FastAPI()
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/cert/verify/{cert_no}", tags=["Cert"])
def read_root(cert_no: str):
   #security_obj = Security()
   #attempts = security_obj.track_attempts(cert_no)
        return logic.verify_cert(cert_no)

class Certificate(BaseModel):
    name: str
    middle_name: str
    surname: str
      
@router.post("/cert/generate", tags=["Cert"])
async def read_root(certificate: Certificate):
    cert = logic.create_cert(certificate.name, certificate.middle_name, certificate.surname)
    return {"data": f"Generated certificate number: {cert}"}

@router.get("/cert/{cert_no}", tags=["Cert"])
def read_root(cert_no: str):
    
    cert = logic.get_cert_by_no(cert_no)
    if cert:
        return {"data": cert}
    else:
        return {"data": f"Certificate number: {cert_no} is invalid."}


@router.post("/auth/register", tags=["Auth"])
async def register_user(register: AuthRegister):
    
    try:
        user = auth.register(register)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    return {
        "data": {
            "email": register.email,
            "password": register.password,
            "username": user["username"],
            "isOnline": user["isOnline"],
            "message": "User registered successfully."
        }
    }

@router.post("/auth/login", tags=["Auth"])
async def login_user(login: AuthLogin):

    try:
        account = auth.login(login.email, login.password)
        return {
            "data": account
        }  

    except ValueError as e:
         raise HTTPException(status_code=401, detail=str(e))
        
@router.post("/auth/users", tags=["Auth"])
async def list_users_endpoint(token: Token):
    try:
        payload = jwt.decode(token.jwt, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid subject in token")
        
        for user in auth.list_users():
            if user['email'] == email:
                break
        else:
            raise HTTPException(status_code=401, detail="Unauthorized user")
        
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    users = auth.list_users()
    return {
        "data": {
            "users": users
        }
    }  

@router.post("/auth/logout", tags=["Auth"])
async def logout_user():
    return {
        "data": { 
            "isOnline": False,
            "message": "User logged out successfully."
        }
    }

app.include_router(router)