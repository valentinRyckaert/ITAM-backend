from fastapi import Depends, FastAPI, HTTPException, Query, status, APIRouter
from typing import Annotated
from ..db.database import Package
from ..dependencies import SessionDep, engine
from sqlmodel import select
from ..internal.auth import get_current_user, verify_access

import os

router = APIRouter(
    prefix="/packages",
    tags=["packages"],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
def create_package(package: Package, session: SessionDep):
    verify_access(1)
    if session.get(Package, package.PACK_id):
        return HTTPException(status_code=400, detail="Package id already exists")
    session.add(package)
    session.commit()
    session.refresh(package)
    return package

@router.get("/", response_model=list[Package])
def read_packages(session: SessionDep) -> list[Package]:
    verify_access(2)
    return session.exec(select(Package)).all()

@router.get("/{package_id}/")
def read_package(package_id: int, session: SessionDep):
    verify_access(2)
    package = session.get(Package, package_id)
    if not package:
        return HTTPException(status_code=404, detail="Package not found")
    return package

@router.put("/{package_id}/")
def update_package(package_id: int, package: Package, session: SessionDep):
    verify_access(1)
    db_package = session.get(Package, package_id)
    if not db_package:
        return HTTPException(status_code=404, detail="Package not found")
    
    db_package.PACK_name = package.P_name
    db_package.PACK_type = package.P_type
    db_package.PACK_os_supported = package.P_os_supported
    db_package.DEV_id = package.DEV_id
    db_package.DG_id = package.DG_id
    db_package.PG_id = package.PG_id
    
    session.add(db_package)
    session.commit()
    session.refresh(db_package)
    
    return db_package

@router.delete("/{package_id}/delete/")
def delete_package(package_id: int, session: SessionDep):
    verify_access(1)
    package = session.get(Package, package_id)
    if not package:
        return HTTPException(status_code=404, detail="Package not found")
    
    session.delete(package)
    session.commit()
    
    return {"detail": "Package deleted successfully"}

@router.get("/autoupdate")
def auto_update(session: SessionDep):
    verify_access(1)
    filenameInDB = []
    for packageInDB in session.exec(select(Package)).all():
        filenameInDB.append(packageInDB.PACK_name)
    fichiers = os.listdir("db/deploy/")
    for fichier in fichiers:
        if os.path.isfile(os.path.join("db/deploy/", fichier)) and not (fichier in filenameInDB):
            nom, extension = os.path.splitext(fichier)
            package = Package(
                PACK_id = 8395839,
                PACK_name = nom,
                PACK_type = extension,
                PACK_os_supported = "any"
            )
            session.add(package)
            session.commit()
            session.refresh(package)
    return {"detail":"autoupdate successful"}
