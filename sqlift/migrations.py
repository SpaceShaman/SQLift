import sqlite3


def up(migration_name: str) -> None:
    with sqlite3.connect("db.sqlite") as connection:
        cursor = connection.cursor()
        cursor.execute(_get_sql_up_command(migration_name))


def _get_sql_up_command(migration_name: str) -> str:
    sql = open(f"migrations/{migration_name}.sql").read()
    return sql.split("--DOWN")[0]
