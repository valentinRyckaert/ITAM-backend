from sqlmodel import Field, SQLModel, String, Column, TEXT
from typing import Optional

class DeviceGroup(SQLModel, table=True):
    DG_id: Optional[int] = Field(default=None, index=True, primary_key=True)
    DG_libelle: str = Field(index=True, sa_type=TEXT)

class Device(SQLModel, table=True):
    DEV_id: Optional[int] = Field(default=None, index=True, primary_key=True)
    DEV_name: str = Field(index=True, sa_type=TEXT)
    DEV_os: str = Field(index=True, sa_type=TEXT)
    DG_id: int | None = Field(default=None, index=True, foreign_key="devicegroup.DG_id")

class PackageGroup(SQLModel, table=True):
    PG_id: Optional[int] = Field(default=None, index=True, primary_key=True)
    PG_libelle: str = Field(index=True, sa_type=TEXT)

class Package(SQLModel, table=True):
    PACK_id: Optional[int] = Field(default=None, index=True, primary_key=True)
    PACK_name: str = Field(index=True, sa_type=TEXT)
    PACK_type: str = Field(index=True, sa_type=TEXT)
    PACK_os_supported: str = Field(index=True, sa_type=TEXT)
    DEV_id: int | None = Field(default=None, index=True, foreign_key="device.DEV_id")
    DG_id: int | None = Field(default=None, index=True, foreign_key="devicegroup.DG_id")
    PG_id: int | None = Field(default=None, index=True, foreign_key="packagegroup.PG_id")

class User(SQLModel, table=True):
    USER_id: Optional[int] = Field(default=None, index=True, primary_key=True)
    USER_username: str = Field(index=True, sa_type=TEXT)
    USER_passHash: str = Field(index=True, sa_type=TEXT)
    USER_type: int = Field(index=True)
    USER_isActive: bool = Field(index=True)

def create_db(engine):
    SQLModel.metadata.create_all(engine)
