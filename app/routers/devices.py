from fastapi import Depends, FastAPI, HTTPException, Query, status, APIRouter
from typing import Annotated
from ..db.database import Device, User
from ..dependencies import SessionDep, engine
from sqlmodel import select

from fastapi.responses import FileResponse
from ..internal.auth import get_current_user, verify_access

router = APIRouter(
    prefix="/devices",
    tags=["devices"],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def read_devices(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100
):
    verify_access(2)
    devices = session.exec(select(Device).offset(offset).limit(limit)).all()
    return devices

@router.post("/")
def create_device(device: Device, session: SessionDep):
    verify_access(1)
    if session.get(Device, device.DEV_id):
        return HTTPException(status_code=400, detail="Device id already exists")
    session.add(device)
    session.commit()
    session.refresh(device)
    return device

@router.get("/{device_id}/")
def read_device(device_id: int, session: SessionDep):
    verify_access(2)
    device = session.get(Device, device_id)
    if not device:
        return HTTPException(status_code=404, detail="Device not found")
    return device

@router.put("/{device_id}/")
def update_device(device_id: int, device: Device, session: SessionDep):
    verify_access(1)
    db_device = session.get(Device, device_id)
    if not db_device:
        return HTTPException(status_code=404, detail="Device not found")
    db_device.DEV_name = device.DEV_name
    db_device.DEV_os = device.DEV_os
    db_device.DG_id = device.DG_id
    session.add(db_device)
    session.commit()
    session.refresh(db_device)
    return db_device

@router.delete("/{device_id}/delete/")
def delete_device(device_id: int, session: SessionDep):
    verify_access(1)
    device = session.get(Device, device_id)
    if not device:
        return HTTPException(status_code=404, detail="Device not found")
    session.delete(device)
    session.commit()
    return {"detail": "Device deleted successfully"}

@router.get("/{device_id}/deploy")
def download_packages(device_id: int, session: SessionDep):
    verify_access(1)
    for package in session.exec(select(Package).where(Package.P_for_device_id == device_id)):
        yield FileResponse(f"./deploy/{package.path}", media_type=package.type, filename=package.name)