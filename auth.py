import random
from datetime import date, timedelta, datetime, timezone
from pydantic import BaseModel
import jwt


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "b6c992167637afd8d25b8ceea99fb423b002429320a2d792ea58938ce1521670"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class TokenData(BaseModel):
    username: str | None = None

class Token(BaseModel):
    access_token: str
    token_type: str


# Global list to registered users
auth_list = []

def verify_cert(cert_no: str):
    if cert_no[:3] in ['NCC', 'GRN']:
        return {"message": "Certificate number is valid."}
    else:
        return {"message": f"Certificate number: {cert_no} is invalid."}
     
def create_username(email: str):
    """
    Create a valid username from email address
    by taking the part before the @ symbol and appending board to it

    eg. email: pdgmawi@gmail.com

    pdmgawi@gmail.com -> 18 Characters

    [pdmgawi,@gmail.com] -> 2 parts

    [0] -> pdmgawi
    [1] -> @gmail.com

    """

    board = random.choice(['NCC', 'GRN']).lower()
    username = email.split('@')[0]
    
    return f"{username}_{board}"
    

def register(register: dict):
    username = create_username(register.email)

    #Avoid Duplicate Usernames
    for user in auth_list:
        if user['email'] == register.email:
            raise ValueError("User already exists")

    #Todays date
    today = date.today()

    # Generate a unique ID for the user
    user_id = len(auth_list) + 1

    user = dict(
            id=user_id,
            username=username,
            email=register.email,
            password=register.password,
            isOnline=False,
        )
    
    # Add user to the global list
    auth_list.append(user)
    
    return user

def list_users():
    """
    Returns a list of all user
    """
    return auth_list


def login(email: str, password: str):


    #Find User by email and password
    for user in auth_list:
        if user['email'] == email and user['password'] == password:
            user['isOnline'] = True

            # Create JWT Token
            access_token = create_access_token(data={"sub": user['email']}, expires_delta=timedelta(minutes=1))
            return {
                "message": "User logged in successfully.",
                "user": {
                    "username": user['username'],
                    "email": user['email'],
                    "isOnline": user['isOnline']
                },
                "token": access_token
            }

    raise ValueError("Invalid email or password")

def get_cert_by_no(cert_no: str):
    """
    Find and return a certificate by certificate number
    """
    for cert in certificates_list:
        if cert.get('cert_no') == cert_no:
            return cert
    return None

def get_certs_by_board(board: str):
    """
    Returns a list of certificates for a specific board
    """
    return [cert for cert in certificates_list if cert.get('board') == board]

def get_certs_by_name(name: str):
    """
    Returns a list of certificates for a specific name
    """
    return [cert for cert in certificates_list if cert.get('name').lower() == name.lower()]

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt