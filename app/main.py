from fastapi import FastAPI
from .routers import devices, device_groups, packages, package_groups, roles, users, files
from .db.database import create_db
from .internal import auth
from .dependencies import *

app = FastAPI()

app.include_router(devices.router)
app.include_router(device_groups.router)
app.include_router(packages.router)
app.include_router(files.router)
app.include_router(package_groups.router)
app.include_router(roles.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.on_event("startup")
def on_startup():
    create_db(engine)
