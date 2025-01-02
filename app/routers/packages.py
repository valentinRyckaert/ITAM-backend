from fastapi import Depends, FastAPI, HTTPException, Query, status, APIRouter
from typing import Annotated
from ..db.database import Package
from ..dependencies import SessionDep, engine
from sqlmodel import select

router = APIRouter(
    prefix="/packages",
    tags=["packages"],
    dependencies=[],
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

@router.get("/{package_id}/", response_model=Package)
def read_package(package_id: int, session: SessionDep) -> Package:
    package = session.get(Package, package_id)
    if not package:
        return HTTPException(status_code=404, detail="Package not found")
    return package

@router.put("/{package_id}/", response_model=Package)
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

@router.delete("/{package_id}/delete/", response_model=dict)
def delete_package(package_id: int, session: SessionDep) -> dict:
    package = session.get(Package, package_id)
    if not package:
        return HTTPException(status_code=404, detail="Package not found")
    
    session.delete(package)
    session.commit()
    
    return {"detail": "Package deleted successfully"}