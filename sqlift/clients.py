import sqlite3
from typing import Protocol


class Cursor(Protocol):
    def fetchone(self): ...


class Client(Protocol):
    def execute(self, sql: str) -> Cursor: ...


def get_client() -> Client:
    return SQLiteClient()


class SQLiteClient:
    def execute(self, sql: str) -> sqlite3.Cursor:
        with sqlite3.connect("db.sqlite") as connection:
            cursor = connection.cursor()
            return cursor.execute(sql)
