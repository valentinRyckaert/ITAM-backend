from fastapi import Depends, FastAPI, HTTPException, Query, status, APIRouter
from typing import Annotated
from ..db.database import PackageGroup
from ..dependencies import SessionDep

router = APIRouter(
    prefix="/packagegroups",
    tags=["package_groups"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=PackageGroup)
def create_package_group(package_group: PackageGroup, session: SessionDep) -> PackageGroup:
    session.add(package_group)
    session.commit()
    session.refresh(package_group)
    return package_group

@router.get("/", response_model=list[PackageGroup])
def read_package_groups(session: SessionDep) -> list[PackageGroup]:
    return session.exec(select(PackageGroup)).all()

@router.get("/{package_group_id}/", response_model=PackageGroup)
def read_package_group(package_group_id: int, session: SessionDep) -> PackageGroup:
    package_group = session.get(PackageGroup, package_group_id)
    if not package_group:
        return HTTPException(status_code=404, detail="device group not found") 
    return package_group

@router.put("/{package_group_id}/", response_model=PackageGroup)
def update_package_group(package_group_id: int, package_group: PackageGroup, session: SessionDep) -> PackageGroup:
    db_package_group = session.get(PackageGroup, package_group_id)
    if not db_package_group:
        return HTTPException(status_code=404, detail="device group not found") 
    
    db_package_group.PG_libelle = package_group.PG_libelle
    session.add(db_package_group)
    session.commit()
    session.refresh(db_package_group)
    
    return db_package_group

@router.delete("/{package_group_id}/delete/", response_model=dict)
def delete_package_group(package_group_id: int, session: SessionDep) -> dict:
    package_group = session.get(PackageGroup, package_group_id)
    if not package_group:
        return HTTPException(status_code=404, detail="device group not found") 
    
    session.delete(package_group)
    session.commit()
    
    return {"detail": "PackageGroup deleted successfully"}