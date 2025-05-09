from fastapi import Request, Depends, FastAPI, HTTPException, APIRouter, UploadFile
from ..internal.auth import verify_access
from ..dependencies import get_current_user
from ..internal.logger import logger
from ..db.database import User
import os
import shutil

router = APIRouter(
    prefix="/files",
    tags=["files"],
    responses={404: {"description": "Not found"}},
)

UPLOAD_DIRECTORY = "app/db/deploy"

@router.post("/")
def create_package(file: UploadFile, request: Request, current_user: User = Depends(get_current_user)):
    """
    Upload a new file package.

    Args:
        file (UploadFile): The file to upload.
        request (Request): The request sent.
        current_user (User): the user who does the request

    Returns:
        str: The filename of the uploaded file.
    """
    verify_access(1)
    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
    if os.path.isfile(file_location):
        logger.warning("File name already exists.", extra={
            'method': request.method,
            'url': request.url.path,
            'status': 'fail',
            'current_user': current_user.USER_username
        })
        raise HTTPException(status_code=400, detail="File name already exists")
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)
    logger.warning("File uploaded successfully.", extra={
        'method': request.method,
        'url': request.url.path,
        'status': 'success',
        'current_user': current_user.USER_username
    })
    return file.filename

@router.delete("/{filename}/delete/")
def delete_file(filename: str, request: Request, current_user: User = Depends(get_current_user)):
    """
    Delete a file by its filename.

    Args:
        filename (str): The name of the file to delete.

    Returns:
        Dict: A success message.
    """
    verify_access(1)
    file_location = os.path.join(UPLOAD_DIRECTORY, filename)
    if os.path.exists(file_location):
        os.remove(file_location)
        logger.warning("File removed successfully.", extra={
            'method': request.method,
            'url': request.url.path,
            'status': 'success',
            'current_user': current_user.USER_username
        })
        return {"status": "removed successfully"}
    logger.warning("File not found.", extra={
        'method': request.method,
        'url': request.url.path,
        'status': 'fail',
        'current_user': current_user.USER_username
    })
    raise HTTPException(status_code=404, detail="File not found")
