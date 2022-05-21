import motor.motor_asyncio
import requests

from typing import Optional, List
from pydantic import BaseModel

from beanie import Document, Indexed, init_beanie

from fastapi import FastAPI, Request, HTTPException

import json
from base64 import b64encode, b64decode


import asyncio
import aiormq
import os


rabbitmq_host = os.environ.get("RABBITMQ_HOST")
rabbitmq_user = os.environ.get("RABBITMQ_USER")
rabbitmq_password = os.environ.get("RABBITMQ_PASSWORD")


class rabbit_body:
    publish_log: dict

    def __init__(self, publish_log):
        self.publish_log = publish_log

    def encode(self):
        dicc = {"publish_log": self.publish_log}
        return b64encode(json.dumps(dicc).encode())

    @staticmethod
    def decode(encoded):
        dicc = json.loads(b64decode(encoded))
        publish_log = dicc["publish_log"]
        return rabbit_body(publish_log)


DATABASE_URL = os.getenv("DATABASE_URI")
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


scipaper = FastAPI(
    openapi_url="/api/v1/paper/openapi.json", docs_url="/api/v1/paper/docs"
)


async def push_to_rabbit(id: str, title: str, author: str):
    request = rabbit_body({"id": id, "title": title, "author": author})

    connection = await aiormq.connect(
        "amqp://{}:{}@{}/".format(rabbitmq_user, rabbitmq_password, rabbitmq_host)
    )

    channel = await connection.channel()

    await channel.basic_publish(
        request.encode(),
        routing_key="publish",
    )


@scipaper.post("/api/v1/paper")
async def create_paper(paper: PaperSchema, request: Request):
    response = requests.get(
        f"http://python_implementation-users_service-1:8000/users/me",
        headers=request.headers,
    )
    if response.status_code != 200:
        raise HTTPException(status_code=403, detail="Unauthorized")
    user = response.json()
    re = await Paper(author=user["email"], title=paper.title, text=paper.text).insert()
    return re


@scipaper.get("/api/v1/paper/{id}")
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
