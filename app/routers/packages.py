from fastapi import Depends, FastAPI, HTTPException, Query, status, APIRouter
from typing import Annotated
from ..db.database import Package
from ..dependencies import SessionDep, engine
from sqlmodel import select
from ..internal.auth import get_current_user

router = APIRouter(
    prefix="/packages",
    tags=["packages"],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=Package)
def create_package(package: Package, session: SessionDep) -> Package:
    session.add(package)
    session.commit()
    session.refresh(package)
    return package

@router.get("/", response_model=list[Package])
def read_packages(session: SessionDep) -> list[Package]:
    return session.exec(select(Package)).all()

@router.get("/{package_id}/")
def read_package(package_id: int, session: SessionDep):
    package = session.get(Package, package_id)
    if not package:
        return HTTPException(status_code=404, detail="Package not found")
    return package

@router.put("/{package_id}/")
def update_package(package_id: int, package: Package, session: SessionDep):
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
    package = session.get(Package, package_id)
    if not package:
        return HTTPException(status_code=404, detail="Package not found")
    
    session.delete(package)
    session.commit()
    
    return {"detail": "Package deleted successfully"}