from fastapi import Depends, FastAPI, HTTPException, Query, status, APIRouter
from typing import Annotated
from ..db.database import PackageGroup
from ..dependencies import SessionDep, engine
from sqlmodel import select
from ..internal.auth import get_current_user

router = APIRouter(
    prefix="/packagegroups",
    tags=["package_groups"],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
def create_package_group(package_group: PackageGroup, session: SessionDep):
    if session.get(PackageGroup, package_group.PG_id):
        return HTTPException(status_code=400, detail="Package group id already exists")
    session.add(package_group)
    session.commit()
    session.refresh(package_group)
    return package_group

@router.get("/", response_model=list[PackageGroup])
def read_package_groups(session: SessionDep) -> list[PackageGroup]:
    return session.exec(select(PackageGroup)).all()

@router.get("/{package_group_id}/")
def read_package_group(package_group_id: int, session: SessionDep):
    package_group = session.get(PackageGroup, package_group_id)
    if not package_group:
        return HTTPException(status_code=404, detail="device group not found") 
    return package_group

@router.put("/{package_group_id}/")
def update_package_group(package_group_id: int, package_group: PackageGroup, session: SessionDep):
    db_package_group = session.get(PackageGroup, package_group_id)
    if not db_package_group:
        return HTTPException(status_code=404, detail="device group not found") 
    
    db_package_group.PG_libelle = package_group.PG_libelle
    session.add(db_package_group)
    session.commit()
    session.refresh(db_package_group)
    
    return db_package_group

@router.delete("/{package_group_id}/delete/")
def delete_package_group(package_group_id: int, session: SessionDep):
    package_group = session.get(PackageGroup, package_group_id)
    if not package_group:
        return HTTPException(status_code=404, detail="device group not found") 
    
    session.delete(package_group)
    session.commit()
    
    return {"detail": "PackageGroup deleted successfully"}