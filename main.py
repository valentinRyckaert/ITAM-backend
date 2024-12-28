from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Session, create_engine, select
from fastapi.responses import FileResponse
from db.database import *

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
engine = create_engine("mariadb+mariadbconnector://<user>:<password>@<host>[:<port>]/<dbname>")
app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db(engine)


@app.post("/devices/")
def create_device(device: Device, session: SessionDep) -> Device:
    session.add(device)
    session.commit()
    session.refresh(device)
    return device


###########
# DEVICES #
###########

@app.get("/devices/", response_model=list[Device])
def read_devices(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Device]:
    devices = session.exec(select(Device).offset(offset).limit(limit)).all()
    return devices

@app.get("/devices/{device_id}", response_model=Device)
def read_device(device_id: int, session: SessionDep = Depends(get_session)) -> Device:
    device = session.get(Device, device_id)
    if not device:
        return {"error" : "no device found"}
    return device

@app.put("/devices/{device_id}", response_model=Device)
def update_device(device_id: int, device: Device, session: SessionDep = Depends(get_session)) -> Device:
    db_device = session.get(Device, device_id)
    if not db_device:
        return {"error" : "no device found"}
    db_device.D_name = device.D_name
    db_device.D_os = device.D_os
    db_device.D_group_device_id = device.D_group_device_id
    session.add(db_device)
    session.commit()
    session.refresh(db_device)
    return db_device

@app.delete("/devices/{device_id}/delete", response_model=dict)
def delete_device(device_id: int, session: SessionDep = Depends(get_session)) -> dict:
    device = session.get(Device, device_id)
    if not device:
        return {"error" : "no device found"}
    session.delete(device)
    session.commit()
    return {"detail": "Device deleted successfully"}

@app.get("/devices/{id}/deploy")
def download_packages(id: int):
    for package in session.exec(select(Package).where(Package.id_device == id)):
        yield FileResponse(f"./deploy/{package.path}", media_type=package.type, filename=package.name)


################
# DEVICE GROUP #
################

@app.post("/devicegroups/", response_model=DeviceGroup)
def create_device_group(device_group: DeviceGroup, session: SessionDep = Depends(get_session)) -> DeviceGroup:
    session.add(device_group)
    session.commit()
    session.refresh(device_group)
    return device_group

@app.get("/devicegroups/", response_model=List[DeviceGroup])
def read_device_groups(session: SessionDep = Depends(get_session)) -> List[DeviceGroup]:
    return session.exec(select(DeviceGroup)).all()

@app.get("/devicegroups/{device_group_id}", response_model=DeviceGroup)
def read_device_group(device_group_id: int, session: SessionDep = Depends(get_session)) -> DeviceGroup:
    device_group = session.get(DeviceGroup, device_group_id)
    if not device_group:
        return {"error" : "no group found"}
    return device_group

@app.put("/devicegroups/{device_group_id}", response_model=DeviceGroup)
def update_device_group(device_group_id: int, device_group: DeviceGroup, session: SessionDep = Depends(get_session)) -> DeviceGroup:
    db_device_group = session.get(DeviceGroup, device_group_id)
    if not db_device_group:
        return {"error" : "no group found"}
    
    db_device_group.DG_libelle = device_group.DG_libelle
    session.add(db_device_group)
    session.commit()
    session.refresh(db_device_group)
    
    return db_device_group

@app.delete("/devicegroups/{device_group_id}/delete", response_model=dict)
def delete_device_group(device_group_id: int, session: SessionDep = Depends(get_session)) -> dict:
    device_group = session.get(DeviceGroup, device_group_id)
    if not device_group:
        return {"error" : "no group found"}
    
    session.delete(device_group)
    session.commit()
    
    return {"detail": "DeviceGroup deleted successfully"}


###########
# PACKAGE #
###########

@app.post("/packages/", response_model=Package)
def create_package(package: Package, session: SessionDep = Depends(get_session)) -> Package:
    session.add(package)
    session.commit()
    session.refresh(package)
    return package

@app.get("/packages/", response_model=List[Package])
def read_packages(session: SessionDep = Depends(get_session)) -> List[Package]:
    return session.exec(select(Package)).all()

@app.get("/packages/{package_id}", response_model=Package)
def read_package(package_id: int, session: SessionDep = Depends(get_session)) -> Package:
    package = session.get(Package, package_id)
    if not package:
        return {"error" : "no package found"}
    return package

@app.put("/packages/{package_id}", response_model=Package)
def update_package(package_id: int, package: Package, session: SessionDep = Depends(get_session)) -> Package:
    db_package = session.get(Package, package_id)
    if not db_package:
        return {"error" : "no package found"}
    
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

@app.delete("/packages/{package_id}/delete", response_model=dict)
def delete_package(package_id: int, session: SessionDep = Depends(get_session)) -> dict:
    package = session.get(Package, package_id)
    if not package:
        return {"error" : "no package found"}
    
    session.delete(package)
    session.commit()
    
    return {"detail": "Package deleted successfully"}

#################
# PACKAGE GROUP #
#################

@app.post("/packagegroups/", response_model=PackageGroup)
def create_package_group(package_group: PackageGroup, session: SessionDep = Depends(get_session)) -> PackageGroup:
    session.add(package_group)
    session.commit()
    session.refresh(package_group)
    return package_group

@app.get("/packagegroups/", response_model=List[PackageGroup])
def read_package_groups(session: SessionDep = Depends(get_session)) -> List[PackageGroup]:
    return session.exec(select(PackageGroup)).all()

@app.get("/packagegroups/{package_group_id}", response_model=PackageGroup)
def read_package_group(package_group_id: int, session: SessionDep = Depends(get_session)) -> PackageGroup:
    package_group = session.get(PackageGroup, package_group_id)
    if not package_group:
        return {"error" : "no group found"}
    return package_group

@app.put("/packagegroups/{package_group_id}", response_model=PackageGroup)
def update_package_group(package_group_id: int, package_group: PackageGroup, session: SessionDep = Depends(get_session)) -> PackageGroup:
    db_package_group = session.get(PackageGroup, package_group_id)
    if not db_package_group:
        return {"error" : "no group found"}
    
    db_package_group.PG_libelle = package_group.PG_libelle
    session.add(db_package_group)
    session.commit()
    session.refresh(db_package_group)
    
    return db_package_group

@app.delete("/packagegroups/{package_group_id}/delete", response_model=dict)
def delete_package_group(package_group_id: int, session: SessionDep = Depends(get_session)) -> dict:
    package_group = session.get(PackageGroup, package_group_id)
    if not package_group:
        return {"error" : "no group found"}
    
    session.delete(package_group)
    session.commit()
    
    return {"detail": "PackageGroup deleted successfully"}


########
# ROLE #
########

@app.post("/roles/", response_model=Role)
def create_role(role: Role, session: SessionDep = Depends(get_session)) -> Role:
    session.add(role)
    session.commit()
    session.refresh(role)
    return role

@app.get("/roles/", response_model=List[Role])
def read_roles(session: SessionDep = Depends(get_session)) -> List[Role]:
    return session.exec(select(Role)).all()

@app.get("/roles/{role_id}", response_model=Role)
def read_role(role_id: int, session: SessionDep = Depends(get_session)) -> Role:
    role = session.get(Role, role_id)
    if not role:
        return {"error" : "no role found"}
    return role

@app.put("/roles/{role_id}", response_model=Role)
def update_role(role_id: int, role: Role, session: SessionDep = Depends(get_session)) -> Role:
    db_role = session.get(Role, role_id)
    if not db_role:
        return {"error" : "no role found"}
    
    db_role.R_libelle = role.R_libelle
    db_role.R_permissions = role.R_permissions
    
    session.add(db_role)
    session.commit()
    session.refresh(db_role)
    
    return db_role

@app.delete("/roles/{role_id}/delete", response_model=dict)
def delete_role(role_id: int, session: SessionDep = Depends(get_session)) -> dict:
    role = session.get(Role,    role_id)
    if not role:
        return {"error" : "no role found"}
    
    session.delete(role)
    session.commit()
    
    return {"detail": "Role deleted successfully"}

########
# USER #
########

@app.post("/users/", response_model=User)
def create_user(user: User, session: SessionDep = Depends(get_session)) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@app.get("/users/", response_model=List[User])
def read_users(session: SessionDep = Depends(get_session)) -> List[User]:
    return session.exec(select(User)).all()

@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, session: SessionDep = Depends(get_session)) -> User:
    user = session.get(User, user_id)
    if not user:
        return {"error" : "no user found"}
    return user

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: User, session: SessionDep = Depends(get_session)) -> User:
    db_user = session.get(User, user_id)
    if not db_user:
        return {"error" : "no user found"}
    
    db_user.U_username = user.U_username
    db_user.U_passHash = user.U_passHash
    db_user.U_role_id = user.U_role_id
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    return db_user

@app.delete("/users/{user_id}/delete", response_model=dict)
def delete_user(user_id: int, session: SessionDep = Depends(get_session)) -> dict:
    user = session.get(User, user_id)
    if not user:
        return {"error" : "no user found"}
    session.delete(user)
    session.commit()
    return {"detail": "User deleted successfully"}

