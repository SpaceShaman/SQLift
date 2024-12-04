import os
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
        with sqlite3.connect(self._get_database_name()) as connection:
            cursor = connection.cursor()
            return cursor.execute(sql)

    def _get_database_name(self) -> str:
        db_url = os.getenv("DB_URL", "sqlite:///db.sqlite")
        return db_url.split("sqlite:///")[-1]
