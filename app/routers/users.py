from fastapi import Request, Depends, FastAPI, HTTPException, Query, status, APIRouter
from typing import Annotated
from ..db.database import User, User
from ..dependencies import SessionDep, engine, get_current_user
from ..internal.logger import logger
from sqlmodel import select
from ..internal.auth import verify_password, create_access_token, get_password_hash, verify_access

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
def create_user(user: User, session: SessionDep, request: Request, current_user: User = Depends(get_current_user)):
    """
    Create a new user.

    Args:
        user (User): The user to create.
        session (SessionDep): The database session.
        request (Request): The request sent.
        current_user (User): the user who does the request

    Returns:
        User: The created user.
    """
    verify_access(0, current_user.USER_type)
    if session.get(User, user.USER_id):
        logger.warning("User id already exists.", extra={
            'method': request.method,
            'url': request.url.path,
            'status': 'fail',
            'user': current_user.USER_username
        })
        raise HTTPException(status_code=400, detail="User id already exists")
    user.USER_passHash = get_password_hash(user.USER_passHash)
    session.add(user)
    session.commit()
    session.refresh(user)
    logger.warning("User created successfully.", extra={
        'method': request.method,
        'url': request.url.path,
        'status': 'success',
        'user': current_user.USER_username
    })
    return user

@router.get("/", response_model=list[User])
def read_users(session: SessionDep, request: Request, current_user: User = Depends(get_current_user)) -> list[User]:
    """
    Retrieve a list of all users.

    Args:
        session (SessionDep): The database session.
        request (Request): The request sent.
        current_user (User): the user who does the request

    Returns:
        List[User]: A list of users.
    """
    verify_access(0, current_user.USER_type)
    users = session.exec(select(User)).all()
    logger.warning("Users read successfully.", extra={
        'method': request.method,
        'url': request.url.path,
        'status': 'success',
        'user': current_user.USER_username
    })
    return users

@router.get("/{user_id}/")
def read_user(user_id: int, session: SessionDep, request: Request, current_user: User = Depends(get_current_user)):
    """
    Retrieve a user by their ID.

    Args:
        user_id (int): The ID of the user.
        session (SessionDep): The database session.
        request (Request): The request sent.
        current_user (User): the user who does the request

    Returns:
        User: The retrieved user.
    """
    verify_access(0, current_user.USER_type)
    user = session.get(User, user_id)
    if not user:
        logger.warning("User not found.", extra={
            'method': request.method,
            'url': request.url.path,
            'status': 'fail',
            'user': current_user.USER_username
        })
        raise HTTPException(status_code=404, detail="User not found")
    logger.warning("User read successfully.", extra={
        'method': request.method,
        'url': request.url.path,
        'status': 'success',
        'user': current_user.USER_username
    })
    return user

@router.put("/{user_id}/")
def update_user(user_id: int, user: User, session: SessionDep, request: Request, current_user: User = Depends(get_current_user)):
    """
    Update an existing user.

    Args:
        user_id (int): The ID of the user to update.
        user (User): The updated user data.
        session (SessionDep): The database session.
        request (Request): The request sent.
        current_user (User): the user who does the request

    Returns:
        User: The updated user.
    """
    verify_access(0, current_user.USER_type)
    db_user = session.get(User, user_id)
    if not db_user:
        logger.warning("User not found.", extra={
            'method': request.method,
            'url': request.url.path,
            'status': 'fail',
            'user': current_user.USER_username
        })
        raise HTTPException(status_code=404, detail="User not found")
    db_user.USER_username = user.USER_username
    db_user.USER_passHash = get_password_hash(user.USER_passHash)
    db_user.USER_type = user.USER_type
    db_user.USER_isActive = user.USER_isActive
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    logger.warning("User updated successfully.", extra={
        'method': request.method,
        'url': request.url.path,
        'status': 'success',
        'user': current_user.USER_username
    })
    return db_user

@router.delete("/{user_id}/delete/")
async def delete_user(user_id: int, session: SessionDep, request: Request, current_user: User = Depends(get_current_user)):
    """
    Delete a user by their ID.

    Args:
        user_id (int): The ID of the user to delete.
        session (SessionDep): The database session.
        request (Request): The request sent.
        current_user (User): the user who does the request

    Returns:
        Dict: A success message.
    """
    await verify_access(0, current_user.USER_type)
    user = session.get(User, user_id)
    if not user:
        logger.warning("User not found.", extra={
            'method': request.method,
            'url': request.url.path,
            'status': 'fail',
            'user': current_user.USER_username
        })
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    logger.warning("User deleted successfully.", extra={
        'method': request.method,
        'url': request.url.path,
        'status': 'success',
        'user': current_user.USER_username
    })
    return {"detail": "User deleted successfully"}
