from fastapi import Depends, FastAPI, HTTPException, APIRouter, UploadFile
from ..internal.auth import verify_access
from ..dependencies import get_current_user
from ..internal.logger import logger
import os
import shutil

router = APIRouter(
    prefix="/files",
    tags=["files"],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}},
)

UPLOAD_DIRECTORY = "app/db/deploy"

@router.post("/")
async def create_package(file: UploadFile):
    """
    Upload a new file package.

    Args:
        file (UploadFile): The file to upload.

    Returns:
        str: The filename of the uploaded file.
    """
    verify_access(1)
    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
    if os.path.isfile(file_location):
        logger.warning("File name already exists.")
        return HTTPException(status_code=400, detail="File name already exists")
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)
    logger.warning("File uploaded successfully.")
    return file.filename

@router.delete("/{filename}/delete/")
def delete_file(filename: str):
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
        logger.warning("File removed successfully.")
        return {"status": "removed successfully"}
    logger.warning("File not found.")
    return HTTPException(status_code=404, detail="File not found")
