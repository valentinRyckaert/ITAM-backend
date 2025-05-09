from fastapi import Request, Depends, FastAPI, HTTPException, Query, status, APIRouter
from typing import Annotated
from ..db.database import User, PackageGroup
from ..dependencies import SessionDep, engine, get_current_user
from ..internal.logger import logger
from sqlmodel import select
from ..internal.auth import verify_access

router = APIRouter(
    prefix="/packagegroups",
    tags=["package_groups"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
def create_package_group(package_group: PackageGroup, session: SessionDep, request: Request, current_user: User = Depends(get_current_user)):
    """
    Create a new package group.

    Args:
        package_group (PackageGroup): The package group to create.
        session (SessionDep): The database session.
        request (Request): The request sent.
        current_user (User): the user who does the request

    Returns:
        PackageGroup: The created package group.
    """
    verify_access(1)
    if session.get(PackageGroup, package_group.PG_id):
        logger.warning("Package group id already exists.", extra={
            'method': request.method,
            'url': request.url.path,
            'status': 'fail',
            'current_user': current_user.USER_username
        })
        raise HTTPException(status_code=400, detail="Package group id already exists")
    session.add(package_group)
    session.commit()
    session.refresh(package_group)
    logger.warning("Package group created successfully.", extra={
        'method': request.method,
        'url': request.url.path,
        'status': 'success',
        'current_user': current_user.USER_username
    })
    return package_group

@router.get("/", response_model=list[PackageGroup])
def read_package_groups(session: SessionDep, request: Request, current_user: User = Depends(get_current_user)) -> list[PackageGroup]:
    """
    Retrieve a list of all package groups.

    Args:
        session (SessionDep): The database session.
        request (Request): The request sent.
        current_user (User): the user who does the request

    Returns:
        List[PackageGroup]: A list of package groups.
    """
    verify_access(2)
    package_groups = session.exec(select(PackageGroup)).all()
    logger.warning("Package groups read successfully.", extra={
        'method': request.method,
        'url': request.url.path,
        'status': 'success',
        'current_user': current_user.USER_username
    })
    return package_groups

@router.get("/{package_group_id}/")
def read_package_group(package_group_id: int, session: SessionDep, request: Request, current_user: User = Depends(get_current_user)):
    """
    Retrieve a package group by its ID.

    Args:
        package_group_id (int): The ID of the package group.
        session (SessionDep): The database session.
        request (Request): The request sent.
        current_user (User): the user who does the request

    Returns:
        PackageGroup: The retrieved package group.
    """
    verify_access(2)
    package_group = session.get(PackageGroup, package_group_id)
    if not package_group:
        logger.warning("Package group not found.", extra={
            'method': request.method,
            'url': request.url.path,
            'status': 'fail',
            'current_user': current_user.USER_username
        })
        raise HTTPException(status_code=404, detail="Package group not found")
    logger.warning("Package group read successfully.", extra={
        'method': request.method,
        'url': request.url.path,
        'status': 'success',
        'current_user': current_user.USER_username
    })
    return package_group

@router.put("/{package_group_id}/")
def update_package_group(package_group_id: int, package_group: PackageGroup, session: SessionDep, request: Request, current_user: User = Depends(get_current_user)):
    """
    Update an existing package group.

    Args:
        package_group_id (int): The ID of the package group to update.
        package_group (PackageGroup): The updated package group data.
        session (SessionDep): The database session.
        request (Request): The request sent.
        current_user (User): the user who does the request

    Returns:
        PackageGroup: The updated package group.
    """
    verify_access(1)
    db_package_group = session.get(PackageGroup, package_group_id)
    if not db_package_group:
        logger.warning("Package group not found.", extra={
            'method': request.method,
            'url': request.url.path,
            'status': 'fail',
            'current_user': current_user.USER_username
        })
        raise HTTPException(status_code=404, detail="Package group not found")
    db_package_group.PG_libelle = package_group.PG_libelle
    session.add(db_package_group)
    session.commit()
    session.refresh(db_package_group)
    logger.warning("Package group updated successfully.", extra={
        'method': request.method,
        'url': request.url.path,
        'status': 'success',
        'current_user': current_user.USER_username
    })
    return db_package_group

@router.delete("/{package_group_id}/delete/")
def delete_package_group(package_group_id: int, session: SessionDep, request: Request, current_user: User = Depends(get_current_user)):
    """
    Delete a package group by its ID.

    Args:
        package_group_id (int): The ID of the package group to delete.
        session (SessionDep): The database session.
        request (Request): The request sent.
        current_user (User): the user who does the request

    Returns:
        Dict: A success message.
    """
    verify_access(1)
    package_group = session.get(PackageGroup, package_group_id)
    if not package_group:
        logger.warning("Package group not found.", extra={
            'method': request.method,
            'url': request.url.path,
            'status': 'fail',
            'current_user': current_user.USER_username
        })
        raise HTTPException(status_code=404, detail="Package group not found")
    session.delete(package_group)
    session.commit()
    logger.warning("Package group deleted successfully.", extra={
        'method': request.method,
        'url': request.url.path,
        'status': 'success',
        'current_user': current_user.USER_username
    })
    return {"detail": "PackageGroup deleted successfully"}
