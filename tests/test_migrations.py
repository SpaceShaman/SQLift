import sqlite3
from datetime import datetime

from sqlift import up


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


# def test_migrate_sqlite_to_latest():
#     os.environ["DATABASE_URL"] = "sqlite:///tests/test.db"
#     conn = sqlite3.connect("tests/test.db")
#     cursor = conn.cursor()

#     up()

#     # check columns in table test
#     result = cursor.execute("PRAGMA table_info(test);").fetchall()

#     assert len(result) == 2
#     assert result[0] == (0, "id", "INTEGER", 0, None, 1)
#     assert result[1] == (1, "name", "TEXT", 0, None, 0)
