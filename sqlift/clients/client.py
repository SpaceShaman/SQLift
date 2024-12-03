from typing import Protocol

from .sqlite import SQLiteClient


class Cursor(Protocol):
    def fetchone(self): ...


class Client(Protocol):
    def execute(self, sql: str) -> Cursor: ...


def get_client() -> Client:
    return SQLiteClient()
