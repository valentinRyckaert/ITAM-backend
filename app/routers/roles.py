from fastapi import Depends, FastAPI, HTTPException, Query, status, APIRouter
from typing import Annotated
from ..db.database import Role
from ..dependencies import SessionDep, engine
from sqlmodel import select

router = APIRouter(
    prefix="/roles",
    tags=["roles"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=Role)
def create_role(role: Role, session: SessionDep) -> Role:
    session.add(role)
    session.commit()
    session.refresh(role)
    return role

@router.get("/", response_model=list[Role])
def read_roles(session: SessionDep) -> list[Role]:
    return session.exec(select(Role)).all()

@router.get("/{role_id}/", response_model=Role)
def read_role(role_id: int, session: SessionDep) -> Role:
    role = session.get(Role, role_id)
    if not role:
        return HTTPException(status_code=404, detail="Role not found")
    return role

@router.put("/{role_id}", response_model=Role)
def update_role(role_id: int, role: Role, session: SessionDep) -> Role:
    db_role = session.get(Role, role_id)
    if not db_role:
        return HTTPException(status_code=404, detail="Role not found")
    
    db_role.R_libelle = role.R_libelle
    db_role.R_permissions = role.R_permissions
    
    session.add(db_role)
    session.commit()
    session.refresh(db_role)
    
    return db_role

@router.delete("/{role_id}/delete/", response_model=dict)
def delete_role(role_id: int, session: SessionDep) -> dict:
    role = session.get(Role,    role_id)
    if not role:
        return HTTPException(status_code=404, detail="Role not found")
    
    session.delete(role)
    session.commit()
    
    return {"detail": "Role deleted successfully"}