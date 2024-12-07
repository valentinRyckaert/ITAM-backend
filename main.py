from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Session, create_engine, select
from fastapi.responses import FileResponse
from db.database import *

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
engine = create_engine("sqlite:///db/database.db", connect_args={"check_same_thread": False})
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

@app.get("/devices/")
def read_devices(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Device]:
    devices = session.exec(select(Device).offset(offset).limit(limit)).all()
    return devices

@app.get("/devices/{device_id}")
def read_device(device_id: int, session: SessionDep) -> Device:
    device = session.get(Device, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="device not found")
    return device

@app.put("/devices/{device_id}")
def update_device(device: Device) -> bool:
    ...

@app.delete("/devices/{device_id}/delete")
def delete_device(device: Device) -> bool:
    ...

@app.get("/devices/{id}/deploy")
def download_packages(id: int):
    for package in session.exec(select(Package).where(Package.id_device == id)):
        yield FileResponse(f"./deploy/{package.path}", media_type=package.type, filename=package.name)


################
# DEVICE GROUP #
################

