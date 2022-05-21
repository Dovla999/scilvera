import motor.motor_asyncio
from beanie import PydanticObjectId
from fastapi_users.db import BeanieBaseUser, BeanieUserDatabase

from pydantic import Field

DATABASE_URL = "mongodb://localhost:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(
    DATABASE_URL, uuidRepresentation="standard"
)
db = client["scipub_python"]


class User(BeanieBaseUser[PydanticObjectId]):
    first_name: str = Field()
    last_name: str = Field()
    pass


async def get_user_db():
    yield BeanieUserDatabase(User)
