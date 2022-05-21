import motor.motor_asyncio
import requests

from typing import Optional, List
from pydantic import BaseModel

from beanie import Document, Indexed, init_beanie, Link

from fastapi import FastAPI, Request, HTTPException
import json
from base64 import b64encode, b64decode

from scipaper import Paper

from rabbit_body import rabbit_body

import asyncio
import aiormq
import os
import datetime

# exchange_name = os.environ.get("EXCHANGE_NAME")
# rabbitmq_host = os.environ.get("RABBITMQ_HOST")
# rabbitmq_user = os.environ.get("RABBITMQ_USER")
# rabbitmq_password = os.environ.get("RABBITMQ_PASSWORD")

exchange_name = "PUBLISH_PAPER"
rabbitmq_host = "localhost"
rabbitmq_user = "guest"
rabbitmq_password = "guest"


library = FastAPI()


class PublishLog(Document):
    paper: Link[Paper] | None
    title: str
    author: str
    date_published: str | None


DATABASE_URL = "mongodb://localhost:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(
    DATABASE_URL, uuidRepresentation="standard"
)
db = client["scipub_python"]


async def on_message(message):
    response = rabbit_body.decode(message.body)
    await PublishLog(
        paper=await Paper.get(response.publish_log["id"]),
        title=response.publish_log["title"],
        author=response.publish_log["author"],
        date_published=str(datetime.datetime.now()),
    ).insert()


async def consume(loop):
    connection = await aiormq.connect(
        "amqp://{}:{}@{}/".format(rabbitmq_user, rabbitmq_password, rabbitmq_host),
        loop=loop,
    )

    channel = await connection.channel()
    declare_ok = await channel.queue_declare("publish")
    consume_ok = await channel.basic_consume(declare_ok.queue, on_message, no_ack=True)


@library.get("/publishings")
async def get_all_published_papers():
    return [
        publish_log
        for publish_log in await PublishLog.find({}, fetch_links=True).to_list()
    ]


@library.on_event("startup")
async def on_startup():
    await init_beanie(
        database=db,
        document_models=[Paper, PublishLog],
    )

    connection = await aiormq.connect(
        "amqp://{}:{}@{}/".format(rabbitmq_user, rabbitmq_password, rabbitmq_host)
    )

    loop = asyncio.get_event_loop()
    asyncio.ensure_future(consume(loop))
