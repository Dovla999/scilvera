from beanie import init_beanie
from fastapi import FastAPI, Depends, Request


from fastapi_users.db import BeanieBaseUser, BeanieUserDatabase, ObjectIDIDMixin


import motor.motor_asyncio
from beanie import PydanticObjectId
import os

from typing import Optional
from pydantic import Field


from fastapi_users import BaseUserManager, FastAPIUsers, schemas
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)


DATABASE_URL = os.getenv("DATABASE_URI")
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


SECRET = "SECRET"


class UserManager(ObjectIDIDMixin, BaseUserManager[User, PydanticObjectId]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")


async def get_user_manager(user_db: BeanieUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, PydanticObjectId](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)


users = FastAPI()

users.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
users.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
users.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


@users.on_event("startup")
async def on_startup():
    await init_beanie(
        database=db,
        document_models=[
            User,
        ],
    )
