import os
from typing import Optional, Protocol, Tuple

from .exceptions import UnsupportedDatabaseError

TupleRow = Tuple


class Cursor(Protocol):
    def fetchone(self) -> Optional[TupleRow]: ...


class Client(Protocol):
    def execute(self, sql: str) -> Cursor: ...


def get_client() -> Client:
    if _is_sqlite():
        return SQLiteClient()
    if _is_postgres():
        return PostgresClient()
    raise UnsupportedDatabaseError("Unsupported database")


def _is_postgres() -> bool:
    return os.getenv("DB_URL", "").startswith("postgresql")


def _is_sqlite() -> bool:
    return os.getenv("DB_URL", "sqlite:///db.sqlite").startswith("sqlite")


class SQLiteClient:
    def execute(self, sql) -> Cursor:
        import sqlite3

        with sqlite3.connect(self._get_database_name()) as connection:
            cursor = connection.cursor()
            for statement in sql.split(";"):
                if statement.strip():
                    cursor.execute(f"{statement};")
            return cursor

    def _get_database_name(self) -> str:
        db_url = os.getenv("DB_URL", "sqlite:///db.sqlite")
        return db_url.split("sqlite:///")[-1]


class PostgresClient:
    def execute(self, sql) -> Cursor:
        import psycopg

        with psycopg.connect(self._get_connection_string()) as connection:
            cursor = connection.cursor()
            return cursor.execute(sql)

    def _get_connection_string(self) -> str:
        return os.getenv("DB_URL", "")
