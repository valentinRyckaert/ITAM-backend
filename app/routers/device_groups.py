from fastapi import Request, Depends, FastAPI, HTTPException, Query, status, APIRouter
from typing import Annotated
from ..db.database import User, DeviceGroup
from ..dependencies import SessionDep, engine, get_current_user
from ..internal.logger import logger
from sqlmodel import select
from ..internal.auth import verify_access

router = APIRouter(
    prefix="/devicegroups",
    tags=["device_groups"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
def create_device_group(device_group: DeviceGroup, session: SessionDep, request: Request, current_user: User = Depends(get_current_user)):
    """
    Create a new device group.

    Args:
        device_group (DeviceGroup): The device group to create.
        session (SessionDep): The database session.
        request (Request): The request sent.
        current_user (User): the user who does the request

    Returns:
        DeviceGroup: The created device group.
    """
    verify_access(1, current_user.USER_type)
    if session.get(DeviceGroup, device_group.DG_id):
        logger.warning("Device group id already exists", extra={
            'method': request.method,
            'url': request.url.path,
            'status': 'fail',
            'current_user': current_user.USER_username
        })
        raise HTTPException(status_code=400, detail="Device group id already exists")
    session.add(device_group)
    session.commit()
    session.refresh(device_group)
    logger.warning("Device group created successfully", extra={
        'method': request.method,
        'url': request.url.path,
        'status': 'success',
        'current_user': current_user.USER_username
    })
    return device_group

@router.get("/", response_model=list[DeviceGroup])
def read_device_groups(session: SessionDep, request: Request, current_user: User = Depends(get_current_user)) -> list[DeviceGroup]:
    """
    Read all device groups.

    Args:
        session (SessionDep): The database session.
        request (Request): The request sent.
        current_user (User): the user who does the request

    Returns:
        list[DeviceGroup]: A list of device groups.
    """
    verify_access(2, current_user.USER_type)
    logger.warning("Reading all device groups", extra={
        'method': request.method,
        'url': request.url.path,
        'status': 'success',
        'current_user': current_user.USER_username
    })
    return session.exec(select(DeviceGroup)).all()

@router.get("/{device_group_id}/")
def read_device_group(device_group_id: int, session: SessionDep, request: Request, current_user: User = Depends(get_current_user)):
    """
    Read a specific device group by ID.

    Args:
        device_group_id (int): The ID of the device group to read.
        session (SessionDep): The database session.
        request (Request): The request sent.
        current_user (User): the user who does the request

    Returns:
        DeviceGroup: The device group with the specified ID.
    """
    verify_access(2, current_user.USER_type)
    device_group = session.get(DeviceGroup, device_group_id)
    if not device_group:
        logger.warning("Device group not found", extra={
            'method': request.method,
            'url': request.url.path,
            'status': 'fail',
            'current_user': current_user.USER_username
        })
        raise HTTPException(status_code=404, detail="device group not found")
    logger.warning("Device group read successfully", extra={
        'method': request.method,
        'url': request.url.path,
        'status': 'success',
        'current_user': current_user.USER_username
    })
    return device_group

@router.put("/{device_group_id}/")
def update_device_group(device_group_id: int, device_group: DeviceGroup, session: SessionDep, request: Request, current_user: User = Depends(get_current_user)):
    """
    Update a specific device group by ID.

    Args:
        device_group_id (int): The ID of the device group to update.
        device_group (DeviceGroup): The updated device group data.
        session (SessionDep): The database session.
        request (Request): The request sent.
        current_user (User): the user who does the request

    Returns:
        DeviceGroup: The updated device group.
    """
    verify_access(1, current_user.USER_type)
    db_device_group = session.get(DeviceGroup, device_group_id)
    if not db_device_group:
        logger.warning("Device group not found", extra={
            'method': request.method,
            'url': request.url.path,
            'status': 'fail',
            'current_user': current_user.USER_username
        })
        raise HTTPException(status_code=404, detail="device group not found")

    db_device_group.DG_libelle = device_group.DG_libelle
    session.add(db_device_group)
    session.commit()
    session.refresh(db_device_group)
    logger.warning("Device group updated successfully", extra={
        'method': request.method,
        'url': request.url.path,
        'status': 'success',
        'current_user': current_user.USER_username
    })
    return db_device_group

@router.delete("/{device_group_id}/delete/")
def delete_device_group(device_group_id: int, session: SessionDep, request: Request, current_user: User = Depends(get_current_user)):
    """
    Delete a specific device group by ID.

    Args:
        device_group_id (int): The ID of the device group to delete.
        session (SessionDep): The database session.
        request (Request): The request sent.
        current_user (User): the user who does the request

    Returns:
        dict: A message indicating the success of the deletion.
    """
    verify_access(1, current_user.USER_type)
    device_group = session.get(DeviceGroup, device_group_id)
    if not device_group:
        logger.warning("Device group not found", extra={
            'method': request.method,
            'url': request.url.path,
            'status': 'fail',
            'current_user': current_user.USER_username
        })
        raise HTTPException(status_code=404, detail="device group not found")

    session.delete(device_group)
    session.commit()
    logger.warning("Device group deleted successfully", extra={
        'method': request.method,
        'url': request.url.path,
        'status': 'success',
        'current_user': current_user.USER_username
    })
    return {"detail": "DeviceGroup deleted successfully"}
