from beanie import PydanticObjectId
from fastapi_users import schemas

from typing import Optional


class UserRead(schemas.BaseUser[PydanticObjectId]):
    first_name: str
    last_name: str
    pass


class UserCreate(schemas.BaseUserCreate):
    first_name: str
    last_name: str
    pass


class UserUpdate(schemas.BaseUserUpdate):
    first_name: Optional[str]
    last_name: Optional[str]
    pass
