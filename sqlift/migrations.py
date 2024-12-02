import sqlite3


def up(migration_name: str) -> None:
    _execute_sql(_get_sql_up_command(migration_name))
    _record_migration(migration_name)


def _get_sql_up_command(migration_name: str) -> str:
    sql = open(f"migrations/{migration_name}.sql").read()
    return sql.split("--DOWN")[0]


def _execute_sql(sql: str) -> None:
    with sqlite3.connect("db.sqlite") as connection:
        cursor = connection.cursor()
        cursor.execute(sql)


def _record_migration(migration_name: str) -> None:
    _create_migrations_table_if_not_exists()
    _execute_sql(
        f"INSERT INTO migrations (migration_name) VALUES ('{migration_name}');"
    )


def _create_migrations_table_if_not_exists() -> None:
    _execute_sql("""
        CREATE TABLE IF NOT EXISTS migrations (
            migration_name TEXT PRIMARY KEY
        );
    """)
