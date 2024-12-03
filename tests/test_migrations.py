import sqlite3
from datetime import datetime

from sqlift import down, up


def get_table_columns(cursor, table_name):
    return cursor.execute(f"PRAGMA table_info({table_name});").fetchall()


def assert_created_at_timestamp(timestamp):
    assert datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S") <= datetime.now()


def assert_columns(
    cursor: sqlite3.Cursor, table_name: str, expected_column_names: list[str]
):
    columns = get_table_columns(cursor, table_name)
    assert len(columns) == len(expected_column_names)
    for i, column in enumerate(columns):
        assert column[1] == expected_column_names[i]


def assert_migration_records(
    cursor: sqlite3.Cursor, expected_migration_records: list[str]
):
    migration_records = cursor.execute("SELECT * FROM migrations;").fetchall()
    assert len(migration_records) == len(expected_migration_records)
    for i, migration_record in enumerate(migration_records):
        assert migration_record[0] == expected_migration_records[i]
        assert_created_at_timestamp(migration_record[1])


def test_migrate_sqlite_to_first_version(cursor):
    up("001_create_test_table")

    assert_columns(cursor, "test", ["id"])
    assert_migration_records(cursor, ["001_create_test_table"])


def test_try_migrate_sqlite_to_first_version_twice(cursor):
    up("001_create_test_table")
    up("001_create_test_table")

    assert_columns(cursor, "test", ["id"])
    assert_migration_records(cursor, ["001_create_test_table"])


def test_migrate_sqlite_to_second_version(cursor):
    up("002_add_name_to_test_table")

    assert_columns(cursor, "test", ["id", "name"])
    assert_migration_records(
        cursor, ["001_create_test_table", "002_add_name_to_test_table"]
    )


def test_migrate_sqlite_to_third_version(cursor):
    up("003_delete_name_from_test_table")

    assert_columns(cursor, "test", ["id"])
    assert_migration_records(
        cursor,
        [
            "001_create_test_table",
            "002_add_name_to_test_table",
            "003_delete_name_from_test_table",
        ],
    )


def test_migrate_sqlite_to_latest(cursor):
    up()

    assert_columns(cursor, "test", ["id"])
    assert_migration_records(
        cursor,
        [
            "001_create_test_table",
            "002_add_name_to_test_table",
            "003_delete_name_from_test_table",
        ],
    )


def test_down_third_version(cursor):
    up()
    down("003_delete_name_from_test_table")

    assert_columns(cursor, "test", ["id", "name"])
    assert_migration_records(
        cursor, ["001_create_test_table", "002_add_name_to_test_table"]
    )


def test_down_second_version(cursor):
    up()
    down("002_add_name_to_test_table")

    assert_columns(cursor, "test", ["id"])
    assert_migration_records(cursor, ["001_create_test_table"])


def test_down_first_version(cursor):
    up()
    down("001_create_test_table")

    assert_columns(cursor, "test", [])
    assert_migration_records(cursor, [])


def test_down_all_versions(cursor):
    up()
    down()

    assert_columns(cursor, "test", [])
    assert_migration_records(cursor, [])
