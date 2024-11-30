from sqlmodel import Field, SQLModel

class DeviceGroup(SQLModel, table=True):
    id: int = Field(default=None, index=True, primary_key=True)
    libelle: str = Field(default=None, index=True)

class Device(SQLModel, table=True):
    id: int = Field(default=None, index=True, primary_key=True)
    name: str = Field(index=True)
    os: int = Field(default=None, index=True)
    group: DeviceGroup = Field(default=None, index=True)

class PackageGroup(SQLModel, table=True):
    id: int = Field(default=None, index=True, primary_key=True)
    libelle: str = Field(default=None, index=True)

class Package(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    path: str = Field(index=True)
    type: str = Field(index=True)
    os_supported: str = Field(default=None, index=True)
    for_device: Device = Field(default=None, index=True)
    for_group: DeviceGroup = Field(default=None, index=True)
    package_group: PackageGroup = Field(default=None, index=True)

class Role(SQLModel, table=True):               
    id: int = Field(default=None, index=True, primary_key=True)
    libelle: str = Field(default=None, index=True)
    permissions: int = Field(default=None, index=True)

class User(SQLModel, table=True):
    id: int = Field(default=None, index=True, primary_key=True)
    username: str = Field(default=None, index=True)
    passHash: str = Field(default=None, index=True)
    role: Role = Field(default=None, index=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
