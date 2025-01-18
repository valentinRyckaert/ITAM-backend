from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import devices, device_groups, packages, package_groups, users, files
from .db.database import create_db
from .internal import auth
from .dependencies import *

app = FastAPI()

origins = [
    "http://localhost:8000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(devices.router)
app.include_router(device_groups.router)
app.include_router(packages.router)
app.include_router(files.router)
app.include_router(package_groups.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.on_event("startup")
def on_startup():
    create_db(engine)
