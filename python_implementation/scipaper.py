import motor.motor_asyncio
import requests

from typing import Optional, List
from pydantic import BaseModel

from beanie import Document, Indexed, init_beanie

from fastapi import FastAPI, Request, HTTPException

import asyncio
import aiormq
import os

# exchange_name = os.environ.get("EXCHANGE_NAME")
# rabbitmq_host = os.environ.get("RABBITMQ_HOST")
# rabbitmq_user = os.environ.get("RABBITMQ_USER")
# rabbitmq_password = os.environ.get("RABBITMQ_PASSWORD")

exchange_name = "PUBLISH_PAPER"
rabbitmq_host = "localhost"
rabbitmq_user = "guest"
rabbitmq_password = "guest"


DATABASE_URL = "mongodb://localhost:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(
    DATABASE_URL, uuidRepresentation="standard"
)
db = client["scipub_python"]


class Section(BaseModel):
    name: str
    content: str


class Paper(Document):
    author: str | None = "Paja patak"
    title: str
    text: List[Section]

    class Settings:
        name = "papers"


class PaperSchema(BaseModel):
    author: str | None = "Paja patak"
    title: str
    text: List[Section]


from fastapi import FastAPI

scipaper = FastAPI()


async def push_to_rabbit(id: str, title: str, author: str):
    request = {"message": {"id": id, "title": title, "author": author}}

    connection = await aiormq.connect(
        "amqp://{}:{}@{}/".format(rabbitmq_user, rabbitmq_password, rabbitmq_host)
    )

    channel = await connection.channel()

    await channel.exchange_declare(exchange=exchange_name, exchange_type="direct")

    await channel.basic_publish(
        request,
        routing_key="publish",
    )


@scipaper.post("/paper")
async def create_paper(paper: PaperSchema, request: Request):
    response = requests.get(f"http://localhost:8000/users/me", headers=request.headers)
    if response.status_code != 200:
        raise HTTPException(status_code=403, detail="Unauthorized")
    user = response.json()
    re = await Paper(author=user["email"], title=paper.title, text=paper.text).insert()
    return re


@scipaper.get("/{id}")
async def publish_paper(id: str):
    try:
        paper = await Paper.get(id)
    except BaseException:
        raise HTTPException(status_code=404, detail="Paper with that id not found")
    await push_to_rabbit(id, paper.title, paper.author)
    return paper


@scipaper.on_event("startup")
async def on_startup():
    await init_beanie(
        database=db,
        document_models=[
            Paper,
        ],
    )
