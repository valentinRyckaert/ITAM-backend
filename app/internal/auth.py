from fastapi import Request, Depends, FastAPI, HTTPException, Query, status, APIRouter
from fastapi.responses import RedirectResponse
from typing import Annotated
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from sqlmodel import select
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..db.database import User, DeviceGroup
from ..dependencies import SessionDep, pwd_context, oauth2_scheme, get_current_user, ALGORITHM, SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, TokenData
from ..internal.logger import logger
from ..db.database import User, User

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

class Token(BaseModel):
    access_token: str
    token_type: str


def verify_password(plain_password, hashed_password):
    """
    Verify a plain password against a hashed password.

    Args:
        plain_password (str): The plain password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """
    Generate a hash for a given password.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create an access token.

    Args:
        data (dict): The data to encode in the token.
        expires_delta (Optional[timedelta]): The expiration time for the token.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def verify_access(accountNumber: int):
    """
    Verify if the current user has the required access level.

    Args:
        accountNumber (int): The required access level.
    """
    if accountNumber < (await get_current_user(SessionDep)).USER_type:
        logger.warning("Incorrect rights.")
        raise HTTPException(status_code=400, detail="Incorrect rights")



@router.post("/login", response_model=Token)
def login(session: SessionDep, request: Request, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    Log in a user and return an access token.

    Args:
        session (SessionDep): The database session.
        form_data (OAuth2PasswordRequestForm): The login form data.

    Returns:
        Token: The access token.
    """
    user = session.exec(select(User).where(User.USER_username == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.USER_passHash):
        logger.warning("Incorrect username or password", extra={
            'method': request.method,
            'url': request.url.path,
            'status': 'fail',
            'user': form_data.username
        })
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": user.USER_username},
        expires_delta=access_token_expires,
    )
    logger.warning("Login successful", extra={
        'method': request.method,
        'url': request.url.path,
        'status': 'fail',
        'user': form_data.username
    })
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=User)
def get_me(current_user: User = Depends(get_current_user)):
    """
    Get the current user's information.

    Args:
        current_user (User): The current user.

    Returns:
        User: The current user's information.
    """
    #logger.warning("User information retrieved successfully.")
    return current_user
