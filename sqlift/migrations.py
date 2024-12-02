import sqlite3


def up(filename: str) -> None:
    sql = open(f"migrations/{filename}.sql").read()

    sql = sql.split("--DOWN")[0]
    with sqlite3.connect("db.sqlite") as connection:
        cursor = connection.cursor()
        cursor.execute(sql)
