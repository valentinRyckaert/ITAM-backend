from sqlmodel import Session, create_engine, select
from typing import Annotated
from pydantic import BaseModel
from fastapi import Depends
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from os import getenv
from dotenv import load_dotenv

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

load_dotenv()
user = getenv('DB_USER')
password = getenv('DB_PASS')
host = getenv('DB_HOST')
dbname = getenv('DB_NAME')

engine = create_engine(
    f"mariadb+mariadbconnector://{user}:{password}@{host}/{dbname}"
)

SECRET_KEY = "your_secret_key"  # Changez cela en une clé secrète sécurisée
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class TokenData(BaseModel):
    username: str

def get_current_user(session: SessionDep, token: str = Depends(oauth2_scheme)):
    """
    Get the current user based on the provided token.

    Args:
        session (SessionDep): The database session.
        token (str): The JWT token.

    Returns:
        User: The current user.
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = session.exec(select(User).where(User.USER_username == token_data.username)).first()
    if user is None:
        raise credentials_exception
    return user