from sqlmodel import Field, SQLModel

class DeviceGroup(SQLModel, table=True):
    DG_id: int = Field(index=True, primary_key=True)
    DG_libelle: str = Field(index=True)

class Device(SQLModel, table=True):
    D_id: int = Field(index=True, primary_key=True)
    D_name: str = Field(index=True)
    D_os: str = Field(index=True)
    D_group_device_id: int | None = Field(default=None, index=True, foreign_key="devicegroup.DG_id")

class PackageGroup(SQLModel, table=True):
    PG_id: int = Field(index=True, primary_key=True)
    PG_libelle: str = Field(index=True)

class Package(SQLModel, table=True):
    P_id: int = Field(index=True, primary_key=True)
    P_name: str = Field(index=True)
    P_path: str = Field(index=True)
    P_type: str = Field(index=True)
    P_os_supported: str = Field(index=True)
    P_for_device_id: int | None = Field(default=None, index=True, foreign_key="device.D_id")
    P_for_group_id: int | None = Field(default=None, index=True, foreign_key="devicegroup.DG_id")
    P_package_group_id: int = Field(default=None, index=True, foreign_key="packagegroup.PG_id")

class Role(SQLModel, table=True):               
    R_id: int = Field(default=None, index=True, primary_key=True)
    R_libelle: str = Field(index=True)
    R_permissions: int = Field(index=True)

class User(SQLModel, table=True):
    U_id: int = Field(index=True, primary_key=True)
    U_username: str = Field(index=True)
    U_passHash: str = Field(index=True)
    U_role_id: int = Field(index=True, foreign_key="role.R_id")


def create_db(engine):
    SQLModel.metadata.create_all(engine)
