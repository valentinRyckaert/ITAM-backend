from fastapi import Depends, FastAPI, HTTPException, APIRouter, UploadFile
from ..internal.auth import get_current_user, verify_access
import os
import shutil

router = APIRouter(
    prefix="/files",
    tags=["files"],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}},
)


UPLOAD_DIRECTORY = "deploy"


@router.post("/")
async def create_package(file: UploadFile):
    verify_access(1)
    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
    if os.path.isfile(file_location):
        return HTTPException(status_code=400, detail="file name already exists")
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return file.filename

@router.delete("/delete/")
def delete_file(filename: str):
    verify_access(1)
    file_location = os.path.join(UPLOAD_DIRECTORY, filename)
    if os.path.exists(file_location):
        os.remove(file_location)
        return {"status" : "removed successfuly"}
    return HTTPException(status_code=404, detail="File not found")

