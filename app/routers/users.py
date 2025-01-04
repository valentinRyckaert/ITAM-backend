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

@router.post("/", response_model=User)
def create_user(user: User, session: SessionDep) -> User:
    user.U_passHash = get_password_hash(user.U_passHash)
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
    
    db_user.U_username = user.U_username
    db_user.U_passHash = user.U_passHash
    db_user.U_role_id = user.U_role_id
    
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
