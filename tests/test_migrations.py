import os
import sqlite3

from sqlift import down, up

from .asserts import assert_columns, assert_migration_records


def test_migrate_sqlite_to_first_version(client):
    up("001_create_test_table")

    assert_columns(client, "test", ["id"])
    assert_migration_records(client, ["001_create_test_table"])


def test_try_migrate_sqlite_to_first_version_twice(client):
    up("001_create_test_table")
    up("001_create_test_table")

    assert_columns(client, "test", ["id"])
    assert_migration_records(client, ["001_create_test_table"])


def test_migrate_sqlite_to_second_version(client):
    up("002_add_name_to_test_table")

    assert_columns(client, "test", ["id", "name"])
    assert_migration_records(
        client, ["001_create_test_table", "002_add_name_to_test_table"]
    )


def test_migrate_sqlite_to_third_version(client):
    up("003_delete_name_from_test_table")

    assert_columns(client, "test", ["id"])
    assert_migration_records(
        client,
        [
            "001_create_test_table",
            "002_add_name_to_test_table",
            "003_delete_name_from_test_table",
        ],
    )


def test_migrate_sqlite_to_latest(client):
    up()

    assert_columns(client, "test", ["id"])
    assert_migration_records(
        client,
        [
            "001_create_test_table",
            "002_add_name_to_test_table",
            "003_delete_name_from_test_table",
        ],
    )


def test_down_third_version(client):
    up()
    down("003_delete_name_from_test_table")

    assert_columns(client, "test", ["id", "name"])
    assert_migration_records(
        client, ["001_create_test_table", "002_add_name_to_test_table"]
    )


def test_down_second_version(client):
    up()
    down("002_add_name_to_test_table")

    assert_columns(client, "test", ["id"])
    assert_migration_records(client, ["001_create_test_table"])


def test_down_first_version(client):
    up()
    down("001_create_test_table")

    assert_columns(client, "test", [])
    assert_migration_records(client, [])


def test_down_all_versions(client):
    up()
    down()

    assert_columns(client, "test", [])
    assert_migration_records(client, [])


def test_try_down_to_not_applied_migration(client):
    up("001_create_test_table")
    down("002_add_name_to_test_table")

    assert_columns(client, "test", ["id"])
    assert_migration_records(client, ["001_create_test_table"])


def test_migrate_sqlite_with_custom_database_name():
    os.environ["DB_URL"] = "sqlite:///custom.db"

    up("001_create_test_table")

    with sqlite3.connect("custom.db") as connection:
        cursor = connection.cursor()
        assert_columns(cursor, "test", ["id"])
        assert_migration_records(cursor, ["001_create_test_table"])
    os.remove("custom.db")
