from sqlmodel import Field, SQLModel

class DeviceGroup(SQLModel, table=True):
    DG_id: int = Field(index=True, primary_key=True)
    DG_libelle: str = Field(index=True)

class Device(SQLModel, table=True):
    DEV_id: int = Field(index=True, primary_key=True)
    DEV_name: str = Field(index=True)
    DEV_os: str = Field(index=True)
    DG_id: int | None = Field(default=None, index=True, foreign_key="devicegroup.DG_id")

class PackageGroup(SQLModel, table=True):
    PG_id: int = Field(index=True, primary_key=True)
    PG_libelle: str = Field(index=True)

class Package(SQLModel, table=True):
    PACK_id: int = Field(index=True, primary_key=True)
    PACK_name: str = Field(index=True)
    PACK_type: str = Field(index=True)
    PACK_os_supported: str = Field(index=True)
    DEV_id: int | None = Field(default=None, index=True, foreign_key="device.DEV_id")
    DG_id: int | None = Field(default=None, index=True, foreign_key="devicegroup.DG_id")
    PG_id: int | None = Field(default=None, index=True, foreign_key="packagegroup.PG_id")

"""
class Role(SQLModel, table=True):               
    ROL_id: int = Field(default=None, index=True, primary_key=True)
    ROL_libelle: str = Field(index=True)
    ROL_perms: int = Field(index=True)
"""

class User(SQLModel, table=True):
    USER_id: int = Field(index=True, primary_key=True)
    USER_username: str = Field(index=True)
    USER_passHash: str = Field(index=True)
    USER_permissions: int = Field(index=True)
    USER_isActive: bool = Field(index=True)
    #ROL_perms: int = Field(index=True, foreign_key="role.ROL_perms")


def create_db(engine):
    SQLModel.metadata.create_all(engine)
