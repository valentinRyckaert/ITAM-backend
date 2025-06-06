from fastapi import Request, Depends, FastAPI, HTTPException, Query, status, APIRouter
from typing import Annotated
from ..db.database import User, Package
from ..dependencies import SessionDep, engine, get_current_user
from ..internal.logger import logger
from sqlmodel import select
from ..internal.auth import verify_access

import os

router = APIRouter(
    prefix="/packages",
    tags=["packages"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
def create_package(package: Package, session: SessionDep, request: Request, current_user: User = Depends(get_current_user)):
    """
    Create a new package.

    Args:
        package (Package): The package to create.
        session (SessionDep): The database session.
        request (Request): The request sent.
        current_user (User): the user who does the request

    Returns:
        Package: The created package.
    """
    verify_access(1, current_user.USER_type)
    if session.get(Package, package.PACK_id):
        logger.warning("Package id already exists.", extra={
            'method': request.method,
            'url': request.url.path,
            'status': 'fail',
            'current_user': current_user.USER_username
        })
        raise HTTPException(status_code=400, detail="Package id already exists")
    session.add(package)
    session.commit()
    session.refresh(package)
    logger.warning("Package created successfully.", extra={
        'method': request.method,
        'url': request.url.path,
        'status': 'success',
        'current_user': current_user.USER_username
    })
    return package

@router.get("/", response_model=list[Package])
def read_packages(session: SessionDep, request: Request, current_user: User = Depends(get_current_user)) -> list[Package]:
    """
    Retrieve a list of all packages.

    Args:
        session (SessionDep): The database session.
        request (Request): The request sent.
        current_user (User): the user who does the request

    Returns:
        List[Package]: A list of packages.
    """
    verify_access(2, current_user.USER_type)
    packages = session.exec(select(Package)).all()
    logger.warning("Packages read successfully.", extra={
        'method': request.method,
        'url': request.url.path,
        'status': 'success',
        'current_user': current_user.USER_username
    })
    return packages

@router.get("/{package_id}/")
def read_package(package_id: int, session: SessionDep, request: Request, current_user: User = Depends(get_current_user)):
    """
    Retrieve a package by its ID.

    Args:
        package_id (int): The ID of the package.
        session (SessionDep): The database session.
        request (Request): The request sent.
        current_user (User): the user who does the request

    Returns:
        Package: The retrieved package.
    """
    verify_access(2, current_user.USER_type)
    package = session.get(Package, package_id)
    if not package:
        logger.warning("Package not found.", extra={
            'method': request.method,
            'url': request.url.path,
            'status': 'fail',
            'current_user': current_user.USER_username
        })
        raise HTTPException(status_code=404, detail="Package not found")
    logger.warning("Package read successfully.", extra={
        'method': request.method,
        'url': request.url.path,
        'status': 'success',
        'current_user': current_user.USER_username
    })
    return package

@router.put("/{package_id}/")
def update_package(package_id: int, package: Package, session: SessionDep, request: Request, current_user: User = Depends(get_current_user)):
    """
    Update an existing package.

    Args:
        package_id (int): The ID of the package to update.
        package (Package): The updated package data.
        session (SessionDep): The database session.
        request (Request): The request sent.
        current_user (User): the user who does the request

    Returns:
        Package: The updated package.
    """
    verify_access(1, current_user.USER_type)
    db_package = session.get(Package, package_id)
    if not db_package:
        logger.warning("Package not found.", extra={
            'method': request.method,
            'url': request.url.path,
            'status': 'fail',
            'current_user': current_user.USER_username
        })
        raise HTTPException(status_code=404, detail="Package not found")
    db_package.PACK_name = package.PACK_name
    db_package.PACK_type = package.PACK_type
    db_package.PACK_os_supported = package.PACK_os_supported
    db_package.DEV_id = package.DEV_id
    db_package.DG_id = package.DG_id
    db_package.PG_id = package.PG_id
    session.add(db_package)
    session.commit()
    session.refresh(db_package)
    logger.warning("Package updated successfully.", extra={
        'method': request.method,
        'url': request.url.path,
        'status': 'success',
        'current_user': current_user.USER_username
    })
    return db_package

@router.delete("/{package_id}/delete/")
def delete_package(package_id: int, session: SessionDep, request: Request, current_user: User = Depends(get_current_user)):
    """
    Delete a package by its ID.

    Args:
        package_id (int): The ID of the package to delete.
        session (SessionDep): The database session.
        request (Request): The request sent.
        current_user (User): the user who does the request

    Returns:
        Dict: A success message.
    """
    verify_access(1, current_user.USER_type)
    package = session.get(Package, package_id)
    if not package:
        logger.warning("Package not found.", extra={
            'method': request.method,
            'url': request.url.path,
            'status': 'fail',
            'current_user': current_user.USER_username
        })
        raise HTTPException(status_code=404, detail="Package not found")
    session.delete(package)
    session.commit()
    logger.warning("Package deleted successfully.", extra={
        'method': request.method,
        'url': request.url.path,
        'status': 'success',
        'current_user': current_user.USER_username
    })
    return {"detail": "Package deleted successfully"}

@router.get("/autoupdate")
def auto_update(session: SessionDep, request: Request, current_user: User = Depends(get_current_user)):
    """
    Automatically update packages based on the files in the deploy directory.

    Args:
        session (SessionDep): The database session.
        request (Request): The request sent.
        current_user (User): the user who does the request

    Returns:
        Dict: A success message.
    """
    verify_access(1, current_user.USER_type)
    filesInDB = [packageInDB for packageInDB in session.exec(select(Package)).all()]
    filenamesInDB = [package.PACK_name+package.PACK_type for package in filesInDB]
    fichiers = os.listdir("app/db/deploy/")
    for fichier in fichiers:
        if fichier not in filenamesInDB:
            Fnom, Fextension = os.path.splitext(fichier)
            package = Package(
                PACK_id=None,
                PACK_name=Fnom,
                PACK_type=Fextension,
                PACK_os_supported="any"
            )
            session.add(package)
            session.commit()
            session.refresh(package)
    
    for filename in filenamesInDB:
        if not (os.path.isfile(os.path.join("app/db/deploy/", filename))):
            package = filesInDB[filenamesInDB.index(filename)]
            session.delete(package)
            session.commit()
    logger.warning(f"Autoupdate successful.", extra={
        'method': request.method,
        'url': request.url.path,
        'status': 'success',
        'current_user': current_user.USER_username
    })
    return {"detail": "Autoupdate successful"}
