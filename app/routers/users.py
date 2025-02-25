from fastapi import Depends, FastAPI, HTTPException, Query, status, APIRouter
from typing import Annotated
from ..db.database import User
from ..dependencies import SessionDep, engine, get_current_user
from ..internal.logger import logger
from sqlmodel import select
from ..internal.auth import verify_password, create_access_token, get_password_hash, verify_access

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
def create_user(user: User, session: SessionDep):
    """
    Create a new user.

    Args:
        user (User): The user to create.
        session (SessionDep): The database session.

    Returns:
        User: The created user.
    """
    verify_access(0)
    if session.get(User, user.USER_id):
        logger.warning("User id already exists.")
        return HTTPException(status_code=400, detail="User id already exists")
    user.USER_passHash = get_password_hash(user.USER_passHash)
    session.add(user)
    session.commit()
    session.refresh(user)
    logger.warning("User created successfully.")
    return user

@router.get("/", response_model=list[User])
def read_users(session: SessionDep) -> list[User]:
    """
    Retrieve a list of all users.

    Args:
        session (SessionDep): The database session.

    Returns:
        List[User]: A list of users.
    """
    verify_access(0)
    users = session.exec(select(User)).all()
    logger.warning("Users read successfully.")
    return users

@router.get("/{user_id}/")
def read_user(user_id: int, session: SessionDep):
    """
    Retrieve a user by their ID.

    Args:
        user_id (int): The ID of the user.
        session (SessionDep): The database session.

    Returns:
        User: The retrieved user.
    """
    verify_access(0)
    user = session.get(User, user_id)
    if not user:
        logger.warning("User not found.")
        return HTTPException(status_code=404, detail="User not found")
    logger.warning("User read successfully.")
    return user

@router.put("/{user_id}/")
def update_user(user_id: int, user: User, session: SessionDep):
    """
    Update an existing user.

    Args:
        user_id (int): The ID of the user to update.
        user (User): The updated user data.
        session (SessionDep): The database session.

    Returns:
        User: The updated user.
    """
    verify_access(0)
    db_user = session.get(User, user_id)
    if not db_user:
        logger.warning("User not found.")
        return HTTPException(status_code=404, detail="User not found")
    db_user.USER_username = user.USER_username
    db_user.USER_passHash = user.USER_passHash
    db_user.USER_role_id = user.U_role_id
    db_user.USER_permissions = user.USER_permissions
    db_user.USER_isActive = user.USER_isActive
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    logger.warning("User updated successfully.")
    return db_user

@router.delete("/{user_id}/delete/")
def delete_user(user_id: int, session: SessionDep):
    """
    Delete a user by their ID.

    Args:
        user_id (int): The ID of the user to delete.
        session (SessionDep): The database session.

    Returns:
        Dict: A success message.
    """
    verify_access(0)
    user = session.get(User, user_id)
    if not user:
        logger.warning("User not found.")
        return HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    logger.warning("User deleted successfully.")
    return {"detail": "User deleted successfully"}
