import sqlite3


class SQLiteClient:
    def execute(self, sql: str) -> sqlite3.Cursor:
        with sqlite3.connect("db.sqlite") as connection:
            cursor = connection.cursor()
            return cursor.execute(sql)
