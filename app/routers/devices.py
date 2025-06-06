from fastapi import Request, Depends, FastAPI, HTTPException, Query, status, APIRouter
from typing import Annotated
from ..db.database import User, Device, User, Package
from ..dependencies import SessionDep, engine, get_current_user
from ..internal.logger import logger
from sqlmodel import select

from fastapi.responses import FileResponse
from ..internal.auth import verify_access
import os
import zipfile as zf
import io
from fastapi.responses import StreamingResponse

router = APIRouter(
    prefix="/devices",
    tags=["devices"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
def read_devices(
    session: SessionDep,
    request: Request,
    current_user: User = Depends(get_current_user),
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100
):
    """
    Retrieve a list of devices with pagination.

    Args:
        session (SessionDep): The database session.
        request (Request): The request sent.
        current_user (User): the user who does the request
        offset (int): The offset for pagination.
        limit (int): The limit for pagination.

    Returns:
        List[Device]: A list of devices.
    """
    verify_access(2, current_user.USER_type)
    devices = session.exec(select(Device).offset(offset).limit(limit)).all()
    logger.warning("Devices read successfully.", extra={
        'method': request.method,
        'url': request.url.path,
        'status': 'success',
        'current_user': current_user.USER_username
    })
    return devices

@router.post("/")
def create_device(device: Device, session: SessionDep, request: Request, current_user: User = Depends(get_current_user)):
    """
    Create a new device.

    Args:
        device (Device): The device to create.
        session (SessionDep): The database session.
        request (Request): The request sent.
        current_user (User): the user who does the request

    Returns:
        Device: The created device.
    """
    verify_access(3, current_user.USER_type)
    if session.get(Device, device.DEV_id):
        logger.warning("Device id already exists.", extra={
            'method': request.method,
            'url': request.url.path,
            'status': 'fail',
            'current_user': current_user.USER_username
        })
        raise HTTPException(status_code=400, detail="Device id already exists")
    session.add(device)
    session.commit()
    session.refresh(device)
    logger.warning("Device created successfully.", extra={
        'method': request.method,
        'url': request.url.path,
        'status': 'success',
        'current_user': current_user.USER_username
    })
    return device

@router.get("/{device_id}/")
def read_device(device_id: int, session: SessionDep, request: Request, current_user: User = Depends(get_current_user)):
    """
    Retrieve a device by its ID.

    Args:
        device_id (int): The ID of the device.
        session (SessionDep): The database session.
        request (Request): The request sent.
        current_user (User): the user who does the request

    Returns:
        Device: The retrieved device.
    """
    verify_access(2, current_user.USER_type)
    device = session.get(Device, device_id)
    if not device:
        logger.warning("Device not found.", extra={
            'method': request.method,
            'url': request.url.path,
            'status': 'fail',
            'current_user': current_user.USER_username
        })
        raise HTTPException(status_code=404, detail="Device not found")
    logger.warning("Device read successfully.", extra={
        'method': request.method,
        'url': request.url.path,
        'status': 'success',
        'current_user': current_user.USER_username
    })
    return device

@router.put("/{device_id}/")
def update_device(device_id: int, device: Device, session: SessionDep, request: Request, current_user: User = Depends(get_current_user)):
    """
    Update an existing device.

    Args:
        device_id (int): The ID of the device to update.
        device (Device): The updated device data.
        session (SessionDep): The database session.
        request (Request): The request sent.
        current_user (User): the user who does the request

    Returns:
        Device: The updated device.
    """
    verify_access(3, current_user.USER_type)
    db_device = session.get(Device, device_id)
    if not db_device:
        logger.warning("Device not found.", extra={
            'method': request.method,
            'url': request.url.path,
            'status': 'fail',
            'current_user': current_user.USER_username
        })
        raise HTTPException(status_code=404, detail="Device not found")
    db_device.DEV_name = device.DEV_name
    db_device.DEV_os = device.DEV_os
    db_device.DG_id = device.DG_id
    session.add(db_device)
    session.commit()
    session.refresh(db_device)
    logger.warning("Device updated successfully.", extra={
        'method': request.method,
        'url': request.url.path,
        'status': 'success',
        'current_user': current_user.USER_username
    })
    return db_device

@router.delete("/{device_id}/delete/")
def delete_device(device_id: int, session: SessionDep, request: Request, current_user: User = Depends(get_current_user)):
    """
    Delete a device by its ID.

    Args:
        device_id (int): The ID of the device to delete.
        session (SessionDep): The database session.
        request (Request): The request sent.
        current_user (User): the user who does the request

    Returns:
        Dict: A success message.
    """
    verify_access(1, current_user.USER_type)
    device = session.get(Device, device_id)
    if not device:
        logger.warning("Device not found.", extra={
            'method': request.method,
            'url': request.url.path,
            'status': 'fail',
            'current_user': current_user.USER_username
        })
        raise HTTPException(status_code=404, detail="Device not found")
    session.delete(device)
    session.commit()
    logger.warning("Device deleted successfully.", extra={
        'method': request.method,
        'url': request.url.path,
        'status': 'success',
        'current_user': current_user.USER_username
    })
    return {"detail": "Device deleted successfully"}

def zipfiles(filenames):
    """
    Create a zip archive from a list of filenames.

    Args:
        filenames (List[str]): The list of filenames to include in the zip archive.

    Returns:
        StreamingResponse: The zip archive as a streaming response.
    """
    zip_io = io.BytesIO()
    with zf.ZipFile(zip_io, mode='w', compression=zf.ZIP_DEFLATED) as temp_zip:
        for name in filenames:
            temp_zip.write(f"db/deploy/{name}")
    return StreamingResponse(
        iter([zip_io.getvalue()]),
        media_type="application/x-zip-compressed",
        headers = { "Content-Disposition": f"attachment; filename=archive.zip"}
    )

@router.get("/{device_id}/deploy")
def download_packages(device_id: int, session: SessionDep, request: Request, current_user: User = Depends(get_current_user)):
    """
    Download packages for a device.

    Args:
        device_id (int): The ID of the device.
        session (SessionDep): The database session.
        request (Request): The request sent.
        current_user (User): the user who does the request

    Returns:
        StreamingResponse: The zip archive containing the packages.
    """
    verify_access(3, current_user.USER_type)
    filepaths = []
    for package in session.exec(select(Package).where(Package.DEV_id == device_id)):
        filepaths.append(package.PACK_name)
    logger.warning("Packages downloaded successfully.", extra={
        'method': request.method,
        'url': request.url.path,
        'status': 'success',
        'current_user': current_user.USER_username
    })
    return zipfiles(filepaths)
