from fastapi import Depends, FastAPI, HTTPException, Query, status, APIRouter, UploadFile, File
from typing import Annotated
from ..db.database import Package
from ..dependencies import SessionDep, engine
from sqlmodel import select
from ..internal.auth import get_current_user
import os
import shutil

router = APIRouter(
    prefix="/files",
    tags=["files"],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}},
)


UPLOAD_DIRECTORY = "./deploy"


@router.post("/")
async def create_package(file: UploadFile):
    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return file.filename

@router.delete("/delete/", response_model=dict)
def delete_file(filename: str):
    if os.path.exists(os.path.join(UPLOAD_DIRECTORY, filename)):
        os.remove(os.path.join(UPLOAD_DIRECTORY, filename))
    return {"status" : "removed successfuly"}

