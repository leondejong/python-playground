import sqlite3

from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

connection = sqlite3.connect("list.db")
cursor = connection.cursor()
app = FastAPI()


class Item(BaseModel):
    id: Union[int, None] = None
    name: Union[str, None] = None
    content: Union[str, None] = None
    active: bool = False


def create_table():
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS list (
          id INTEGER PRIMARY KEY,
          name TEXT,
          content TEXT,
          active INTEGER
        )
        """
    )


def select_list():
    return cursor.execute(
        """
        SELECT * FROM list
        """
    ).fetchall()


def select_item(id):
    return cursor.execute(
        """
        SELECT * FROM list
        WHERE id=? LIMIT 1
        """,
        str(id),
    ).fetchone()


def insert_item(name, content, active):
    cursor.execute(
        """
        INSERT INTO list
        VALUES (?, ?, ?, ?)
        """,
        (None, name, content, active),
    )
    connection.commit()


def update_item(id, name=None, content=None, active=None):
    cursor.execute(
        """
        UPDATE list SET
          name    = coalesce(?, name),
          content = coalesce(?, content),
          active  = coalesce(?, active)
        WHERE id=?
        """,
        (name, content, active, str(id)),
    )
    connection.commit()


def delete_item(id):
    cursor.execute(
        """
        DELETE FROM list WHERE id=?
        """,
        str(id),
    )
    connection.commit()


@app.get("/")
async def index():
    return select_list()


@app.get("/{id}")
async def fetch(id: int):
    return select_item(id)


@app.post("/")
async def create(item: Item):
    return insert_item(item.name, item.content, item.active)


@app.put("/{id}")
@app.patch("/{id}")
async def update(id: int, item: Item):
    return update_item(id, item.name, item.content, item.active)


@app.delete("/{id}")
async def remove(id: int):
    return delete_item(id)
