from contextlib import asynccontextmanager

import psycopg
from fastapi import FastAPI
from pydantic import BaseModel

from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    with psycopg.connect(settings.database_url) as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS messages ("
            "id SERIAL PRIMARY KEY, "
            "author TEXT NOT NULL, "
            "text TEXT NOT NULL, "
            "created_at TIMESTAMPTZ DEFAULT now())"
        )
    yield


app = FastAPI(title="Guestbook", lifespan=lifespan)


class MessageIn(BaseModel):
    author: str
    text: str


@app.get("/health")
def health():
    return {"status": "ok", "version": settings.app_version}


@app.get("/messages")
def list_messages():
    with psycopg.connect(settings.database_url) as conn:
        rows = conn.execute(
            "SELECT id, author, text FROM messages ORDER BY id DESC"
        ).fetchall()
    return [{"id": r[0], "author": r[1], "text": r[2]} for r in rows]


@app.post("/messages")
def add_message(m: MessageIn):
    with psycopg.connect(settings.database_url) as conn:
        row = conn.execute(
            "INSERT INTO messages (author, text) VALUES (%s, %s) RETURNING id",
            (m.author, m.text),
        ).fetchone()
    return {"id": row[0], "author": m.author, "text": m.text}


@app.get("/")
def root():
    return {"app": "guestbook", "version": settings.app_version}
