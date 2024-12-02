from sqlift import up


def test_migrate_sqlite_to_first_version(cursor):
    up("001_create_test_table")

    result = cursor.execute("PRAGMA table_info(test);").fetchall()

    assert len(result) == 1
    assert result[0] == (0, "id", "INTEGER", 0, None, 1)


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
