from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query, Request, status
from sqlmodel import Session, create_engine, select
from fastapi.responses import FileResponse
from .db.database import *
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import Security
from fastapi.security import OAuth2PasswordRequestForm
from typing import Optional
from pydantic import BaseModel
from .routers import devices, device_groups, packages, package_groups, roles, users
from .internal import auth
from .dependencies import *


SECRET_KEY = "your_secret_key"  # Changez cela en une clé secrète sécurisée
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


app = FastAPI()

app.include_router(devices.router)
app.include_router(device_groups.router)
app.include_router(packages.router)
app.include_router(package_groups.router)
app.include_router(roles.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.on_event("startup")
def on_startup():
    create_db(engine)
