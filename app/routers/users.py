from fastapi import Depends, FastAPI, HTTPException, Query, status, APIRouter
from typing import Annotated
from ..db.database import User
from ..dependencies import SessionDep, engine
from sqlmodel import select
from ..internal.auth import verify_password, create_access_token, get_password_hash, get_current_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
def create_user(user: User, session: SessionDep):
    if session.get(User, user.USER_id):
        return HTTPException(status_code=400, detail="User id already exists")
    user.USER_passHash = get_password_hash(user.USER_passHash)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.get("/", response_model=list[User])
def read_users(session: SessionDep) -> list[User]:
    return session.exec(select(User)).all()

@router.get("/{user_id}/")
def read_user(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        return HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}/")
def update_user(user_id: int, user: User, session: SessionDep):
    db_user = session.get(User, user_id)
    if not db_user:
        return HTTPException(status_code=404, detail="User not found")
    
    db_user.USER_username = user.USER_username
    db_user.USER_passHash = user.USER_passHash
    db_user.USER_role_id = user.U_role_id
    db_user.USER_permissions = user.USER_permissions
    db_user.USER_isActive = user.USER_isActive
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    return db_user

@router.delete("/{user_id}/delete/")
def delete_user(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        return HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"detail": "User deleted successfully"}
