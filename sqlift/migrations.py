import sqlite3
from pathlib import Path


def up(target_migration: str | None = None) -> None:
    _create_migrations_table_if_not_exists()
    for migration_name in _get_migration_names(target_migration):
        if _is_migration_recorded(migration_name):
            return
        _execute_sql(_get_sql_up_command(migration_name))
        _record_migration(migration_name)


def _get_migration_names(target_migration: str | None) -> list[str]:
    migration_names = sorted(
        [migration_path.stem for migration_path in Path("migrations").glob("*.sql")]
    )
    if target_migration:
        return migration_names[: migration_names.index(target_migration) + 1]
    return migration_names


def _get_sql_up_command(migration_name: str) -> str:
    sql = open(f"migrations/{migration_name}.sql").read()
    return sql.split("--DOWN")[0]


def _execute_sql(sql: str) -> sqlite3.Cursor:
    with sqlite3.connect("db.sqlite") as connection:
        cursor = connection.cursor()
        return cursor.execute(sql)


def _record_migration(migration_name: str) -> None:
    _execute_sql(
        f"INSERT INTO migrations (migration_name) VALUES ('{migration_name}');"
    )


def _create_migrations_table_if_not_exists() -> None:
    _execute_sql("""
        CREATE TABLE IF NOT EXISTS migrations (
            migration_name TEXT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)


def _is_migration_recorded(migration_name: str) -> bool:
    return (
        _execute_sql(
            f"SELECT * FROM migrations WHERE migration_name = '{migration_name}';"
        ).fetchone()
        is not None
    )
