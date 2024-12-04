import os
from datetime import datetime
from typing import Protocol


class Assertor(Protocol):
    def assert_columns(self, table_name: str, expected_column_names: list[str]): ...
    def assert_migration_records(self, expected_migration_records: list[str]): ...


class SQLiteAssertor:
    def __init__(self, client):
        self.client = client

    def assert_columns(self, table_name: str, expected_column_names: list[str]):
        columns = self._get_table_columns(table_name)
        assert len(columns) == len(expected_column_names)
        for i, column in enumerate(columns):
            assert column[1] == expected_column_names[i]

    def assert_migration_records(self, expected_migration_records: list[str]):
        migration_records = self.client.execute("SELECT * FROM migrations;").fetchall()
        assert len(migration_records) == len(expected_migration_records)
        for i, migration_record in enumerate(migration_records):
            assert migration_record[0] == expected_migration_records[i]
            self._assert_created_at_timestamp(migration_record[1])

    def _get_table_columns(self, table_name):
        return self.client.execute(f"PRAGMA table_info({table_name});").fetchall()

    def _assert_created_at_timestamp(self, timestamp):
        assert datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S") <= datetime.now()


class PostgresAssertor:
    def __init__(self, client):
        self.client = client

    def assert_columns(self, table_name: str, expected_column_names: list[str]):
        columns = self._get_table_columns(table_name)
        assert len(columns) == len(expected_column_names)
        for i, column in enumerate(columns):
            assert column[0] == expected_column_names[i]

    def assert_migration_records(self, expected_migration_records: list[str]):
        migration_records = self.client.execute("SELECT * FROM migrations;").fetchall()
        assert len(migration_records) == len(expected_migration_records)
        for i, migration_record in enumerate(migration_records):
            assert migration_record[0] == expected_migration_records[i]
            assert migration_record[1] <= datetime.now()

    def _get_table_columns(self, table_name):
        return self.client.execute(
            f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}';"
        ).fetchall()


def assert_columns(client, table_name: str, expected_column_names: list[str]):
    assertor = _get_assertor(client)
    assertor.assert_columns(table_name, expected_column_names)


def assert_migration_records(client, expected_migration_records: list[str]):
    assertor = _get_assertor(client)
    assertor.assert_migration_records(expected_migration_records)


def _get_assertor(client) -> Assertor:
    if _is_sqlite():
        return SQLiteAssertor(client)
    if _is_postgres():
        return PostgresAssertor(client)
    raise ValueError("Unsupported database")


def _is_sqlite() -> bool:
    return os.getenv("DB_URL", "").startswith("sqlite")


def _is_postgres() -> bool:
    return os.getenv("DB_URL", "").startswith("postgresql")
