from fastapi import Depends, FastAPI, HTTPException, Query, status, APIRouter
from typing import Annotated
from ..db.database import DeviceGroup
from ..dependencies import SessionDep

router = APIRouter(
    prefix="/devicegroups",
    tags=["device_groups"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=DeviceGroup)
def create_device_group(device_group: DeviceGroup, session: SessionDep) -> DeviceGroup:
    session.add(device_group)
    session.commit()
    session.refresh(device_group)
    return device_group

@router.get("/", response_model=list[DeviceGroup])
def read_device_groups(session: SessionDep) -> list[DeviceGroup]:
    return session.exec(select(DeviceGroup)).all()

@router.get("/{device_group_id}/", response_model=DeviceGroup)
def read_device_group(device_group_id: int, session: SessionDep) -> DeviceGroup:
    device_group = session.get(DeviceGroup, device_group_id)
    if not device_group:
        return HTTPException(status_code=404, detail="device group not found") 
    return device_group

@router.put("/{device_group_id}/", response_model=DeviceGroup)
def update_device_group(device_group_id: int, device_group: DeviceGroup, session: SessionDep) -> DeviceGroup:
    db_device_group = session.get(DeviceGroup, device_group_id)
    if not db_device_group:
        return HTTPException(status_code=404, detail="device group not found") 
    
    db_device_group.DG_libelle = device_group.DG_libelle
    session.add(db_device_group)
    session.commit()
    session.refresh(db_device_group)
    
    return db_device_group

@router.delete("/{device_group_id}/delete/", response_model=dict)
def delete_device_group(device_group_id: int, session: SessionDep) -> dict:
    device_group = session.get(DeviceGroup, device_group_id)
    if not device_group:
        return HTTPException(status_code=404, detail="device group not found") 
    
    session.delete(device_group)
    session.commit()
    
    return {"detail": "DeviceGroup deleted successfully"}
