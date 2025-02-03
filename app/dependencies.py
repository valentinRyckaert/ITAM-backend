from sqlmodel import Session, create_engine, select
from typing import Annotated
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