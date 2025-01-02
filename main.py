from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query, Request, status
from sqlmodel import Session, create_engine, select
from fastapi.responses import FileResponse
from db.database import *
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import Security
from fastapi.security import OAuth2PasswordRequestForm
from typing import Optional
from pydantic import BaseModel


SECRET_KEY = "your_secret_key"  # Changez cela en une clé secrète sécurisée
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_session():
    with Session(engine) as session:
        yield session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
SessionDep = Annotated[Session, Depends(get_session)]
engine = create_engine("sqlite:///db/database.db", connect_args={"check_same_thread": False})
app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db(engine)


###########
# DEVICES #
###########

@app.post("/devices/")
def create_device(device: Device, session: SessionDep) -> Device:
    session.add(device)
    session.commit()
    session.refresh(device)
    return device

@app.get("/devices/", response_model=list[Device])
def read_devices(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Device]:
    devices = session.exec(select(Device).offset(offset).limit(limit)).all()
    return devices

@app.get("/devices/{device_id}/", response_model=Device)
def read_device(device_id: int, session: SessionDep) -> Device:
    device = session.get(Device, device_id)
    if not device:
        return HTTPException(status_code=404, detail="Device not found")
    return device

@app.put("/devices/{device_id}/", response_model=Device)
def update_device(device_id: int, device: Device, session: SessionDep) -> Device:
    db_device = session.get(Device, device_id)
    if not db_device:
        return HTTPException(status_code=404, detail="Device not found")
    db_device.D_name = device.D_name
    db_device.D_os = device.D_os
    db_device.D_group_device_id = device.D_group_device_id
    session.add(db_device)
    session.commit()
    session.refresh(db_device)
    return db_device

@app.delete("/devices/{device_id}/delete/", response_model=dict)
def delete_device(device_id: int, session: SessionDep) -> dict:
    device = session.get(Device, device_id)
    if not device:
        return HTTPException(status_code=404, detail="Device not found")
    session.delete(device)
    session.commit()
    return {"detail": "Device deleted successfully"}

################
# DEVICE GROUP #
################

@app.post("/devicegroups/", response_model=DeviceGroup)
def create_device_group(device_group: DeviceGroup, session: SessionDep) -> DeviceGroup:
    session.add(device_group)
    session.commit()
    session.refresh(device_group)
    return device_group

@app.get("/devicegroups/", response_model=list[DeviceGroup])
def read_device_groups(session: SessionDep) -> list[DeviceGroup]:
    return session.exec(select(DeviceGroup)).all()

@app.get("/devicegroups/{device_group_id}/", response_model=DeviceGroup)
def read_device_group(device_group_id: int, session: SessionDep) -> DeviceGroup:
    device_group = session.get(DeviceGroup, device_group_id)
    if not device_group:
        return HTTPException(status_code=404, detail="device group not found") 
    return device_group

@app.put("/devicegroups/{device_group_id}/", response_model=DeviceGroup)
def update_device_group(device_group_id: int, device_group: DeviceGroup, session: SessionDep) -> DeviceGroup:
    db_device_group = session.get(DeviceGroup, device_group_id)
    if not db_device_group:
        return HTTPException(status_code=404, detail="device group not found") 
    
    db_device_group.DG_libelle = device_group.DG_libelle
    session.add(db_device_group)
    session.commit()
    session.refresh(db_device_group)
    
    return db_device_group

@app.delete("/devicegroups/{device_group_id}/delete/", response_model=dict)
def delete_device_group(device_group_id: int, session: SessionDep) -> dict:
    device_group = session.get(DeviceGroup, device_group_id)
    if not device_group:
        return HTTPException(status_code=404, detail="device group not found") 
    
    session.delete(device_group)
    session.commit()
    
    return {"detail": "DeviceGroup deleted successfully"}


###########
# PACKAGE #
###########

@app.post("/packages/", response_model=Package)
def create_package(package: Package, session: SessionDep) -> Package:
    session.add(package)
    session.commit()
    session.refresh(package)
    return package

@app.get("/packages/", response_model=list[Package])
def read_packages(session: SessionDep) -> list[Package]:
    return session.exec(select(Package)).all()

@app.get("/packages/{package_id}/", response_model=Package)
def read_package(package_id: int, session: SessionDep) -> Package:
    package = session.get(Package, package_id)
    if not package:
        return HTTPException(status_code=404, detail="Package not found")
    return package

@app.put("/packages/{package_id}/", response_model=Package)
def update_package(package_id: int, package: Package, session: SessionDep) -> Package:
    db_package = session.get(Package, package_id)
    if not db_package:
        return HTTPException(status_code=404, detail="Package not found")
    
    db_package.P_name = package.P_name
    db_package.P_path = package.P_path
    db_package.P_type = package.P_type
    db_package.P_os_supported = package.P_os_supported
    db_package.P_for_device_id = package.P_for_device_id
    db_package.P_for_group_id = package.P_for_group_id
    db_package.P_package_group_id = package.P_package_group_id
    
    session.add(db_package)
    session.commit()
    session.refresh(db_package)
    
    return db_package

@app.delete("/packages/{package_id}/delete/", response_model=dict)
def delete_package(package_id: int, session: SessionDep) -> dict:
    package = session.get(Package, package_id)
    if not package:
        return HTTPException(status_code=404, detail="Package not found")
    
    session.delete(package)
    session.commit()
    
    return {"detail": "Package deleted successfully"}

#################
# PACKAGE GROUP #
#################

@app.post("/packagegroups/", response_model=PackageGroup)
def create_package_group(package_group: PackageGroup, session: SessionDep) -> PackageGroup:
    session.add(package_group)
    session.commit()
    session.refresh(package_group)
    return package_group

@app.get("/packagegroups/", response_model=list[PackageGroup])
def read_package_groups(session: SessionDep) -> list[PackageGroup]:
    return session.exec(select(PackageGroup)).all()

@app.get("/packagegroups/{package_group_id}/", response_model=PackageGroup)
def read_package_group(package_group_id: int, session: SessionDep) -> PackageGroup:
    package_group = session.get(PackageGroup, package_group_id)
    if not package_group:
        return HTTPException(status_code=404, detail="device group not found") 
    return package_group

@app.put("/packagegroups/{package_group_id}/", response_model=PackageGroup)
def update_package_group(package_group_id: int, package_group: PackageGroup, session: SessionDep) -> PackageGroup:
    db_package_group = session.get(PackageGroup, package_group_id)
    if not db_package_group:
        return HTTPException(status_code=404, detail="device group not found") 
    
    db_package_group.PG_libelle = package_group.PG_libelle
    session.add(db_package_group)
    session.commit()
    session.refresh(db_package_group)
    
    return db_package_group

@app.delete("/packagegroups/{package_group_id}/delete/", response_model=dict)
def delete_package_group(package_group_id: int, session: SessionDep) -> dict:
    package_group = session.get(PackageGroup, package_group_id)
    if not package_group:
        return HTTPException(status_code=404, detail="device group not found") 
    
    session.delete(package_group)
    session.commit()
    
    return {"detail": "PackageGroup deleted successfully"}


########
# ROLE #
########

@app.post("/roles/", response_model=Role)
def create_role(role: Role, session: SessionDep) -> Role:
    session.add(role)
    session.commit()
    session.refresh(role)
    return role

@app.get("/roles/", response_model=list[Role])
def read_roles(session: SessionDep) -> list[Role]:
    return session.exec(select(Role)).all()

@app.get("/roles/{role_id}/", response_model=Role)
def read_role(role_id: int, session: SessionDep) -> Role:
    role = session.get(Role, role_id)
    if not role:
        return HTTPException(status_code=404, detail="Role not found")
    return role

@app.put("/roles/{role_id}", response_model=Role)
def update_role(role_id: int, role: Role, session: SessionDep) -> Role:
    db_role = session.get(Role, role_id)
    if not db_role:
        return HTTPException(status_code=404, detail="Role not found")
    
    db_role.R_libelle = role.R_libelle
    db_role.R_permissions = role.R_permissions
    
    session.add(db_role)
    session.commit()
    session.refresh(db_role)
    
    return db_role

@app.delete("/roles/{role_id}/delete/", response_model=dict)
def delete_role(role_id: int, session: SessionDep) -> dict:
    role = session.get(Role,    role_id)
    if not role:
        return HTTPException(status_code=404, detail="Role not found")
    
    session.delete(role)
    session.commit()
    
    return {"detail": "Role deleted successfully"}

########
# USER #
########

@app.post("/users/", response_model=User)
def create_user(user: User, session: SessionDep) -> User:
    user.U_passHash = get_password_hash(user.U_passHash)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@app.get("/users/", response_model=list[User])
def read_users(session: SessionDep) -> list[User]:
    return session.exec(select(User)).all()

@app.get("/users/{user_id}/", response_model=User)
def read_user(user_id: int, session: SessionDep) -> User:
    user = session.get(User, user_id)
    if not user:
        return HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}/", response_model=User)
def update_user(user_id: int, user: User, session: SessionDep) -> User:
    db_user = session.get(User, user_id)
    if not db_user:
        return HTTPException(status_code=404, detail="User not found")
    
    db_user.U_username = user.U_username
    db_user.U_passHash = user.U_passHash
    db_user.U_role_id = user.U_role_id
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    return db_user

@app.delete("/users/{user_id}/delete/", response_model=dict)
def delete_user(user_id: int, session: SessionDep) -> dict:
    user = session.get(User, user_id)
    if not user:
        return HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"detail": "User deleted successfully"}


########
# AUTH #
########

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(session: SessionDep, token: str = Depends(oauth2_scheme)):
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

    user = session.exec(select(User).where(User.U_username == token_data.username)).first()
    if user is None:
        raise credentials_exception
    return user

@app.post("/login", response_model=Token)
def login(session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = session.exec(select(User).where(User.U_username == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.U_passHash):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"username": user.U_username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/logout")
def logout():
    # Pour une implémentation simple, vous pouvez simplement supprimer le token côté client.
    return {"detail": "Logged out successfully"}

@app.get("/users/me/", response_model=User)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


###################
# SPECIFIC ROUTES #
###################

# deployement
@app.get("/devices/{id}/deploy")
def download_packages(id: int):
    for package in session.exec(select(Package).where(Package.P_for_device_id == id)):
        yield FileResponse(f"./deploy/{package.path}", media_type=package.type, filename=package.name)