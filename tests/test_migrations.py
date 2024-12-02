from datetime import datetime

from sqlift import up


def get_table_columns(cursor, table_name):
    return cursor.execute(f"PRAGMA table_info({table_name});").fetchall()


def assert_created_at_timestamp(timestamp):
    assert datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S") <= datetime.now()


def test_migrate_sqlite_to_first_version(cursor):
    up("001_create_test_table")

    columns = get_table_columns(cursor, "test")
    assert len(columns) == 1
    assert columns[0] == (0, "id", "INTEGER", 0, None, 1)

    migration_records = cursor.execute("SELECT * FROM migrations;").fetchall()
    assert len(migration_records) == 1
    first_migration_record = migration_records[0]
    assert first_migration_record[0] == "001_create_test_table"
    assert_created_at_timestamp(first_migration_record[1])


def test_try_migrate_sqlite_to_first_version_twice(cursor):
    up("001_create_test_table")
    up("001_create_test_table")

    columns = get_table_columns(cursor, "test")
    assert len(columns) == 1
    assert columns[0] == (0, "id", "INTEGER", 0, None, 1)

    migration_records = cursor.execute("SELECT * FROM migrations;").fetchall()
    assert len(migration_records) == 1
    first_migration_record = migration_records[0]
    assert first_migration_record[0] == "001_create_test_table"
    assert_created_at_timestamp(first_migration_record[1])


def test_migrate_sqlite_to_second_version(cursor):
    up("002_add_name_to_test_table")

    columns = get_table_columns(cursor, "test")
    assert len(columns) == 2
    assert columns[0] == (0, "id", "INTEGER", 0, None, 1)
    assert columns[1] == (1, "name", "TEXT", 1, None, 0)

    migration_records = cursor.execute("SELECT * FROM migrations;").fetchall()
    assert len(migration_records) == 2
    first_migration_record = migration_records[0]
    assert first_migration_record[0] == "001_create_test_table"
    assert_created_at_timestamp(first_migration_record[1])
    second_migration_record = migration_records[1]
    assert second_migration_record[0] == "002_add_name_to_test_table"
    assert_created_at_timestamp(second_migration_record[1])


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
