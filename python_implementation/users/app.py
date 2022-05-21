from beanie import init_beanie
from fastapi import Depends, FastAPI

from .db import User, db
from .schemas import UserCreate, UserRead, UserUpdate
from .users import auth_backend, current_active_user, fastapi_users

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
