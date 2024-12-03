from pathlib import Path

from .clients import get_client

client = get_client()


def up(target_migration: str | None = None) -> None:
    _create_migrations_table_if_not_exists()
    for migration_name in _get_migration_names(target_migration):
        _apply_migration(migration_name)


def _apply_migration(migration_name: str) -> None:
    if _is_migration_recorded(migration_name):
        return
    client.execute(_get_sql_up_command(migration_name))
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


def _record_migration(migration_name: str) -> None:
    client.execute(
        f"INSERT INTO migrations (migration_name) VALUES ('{migration_name}');"
    )


def _create_migrations_table_if_not_exists() -> None:
    client.execute("""
        CREATE TABLE IF NOT EXISTS migrations (
            migration_name TEXT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)


def _is_migration_recorded(migration_name: str) -> bool:
    return (
        client.execute(
            f"SELECT * FROM migrations WHERE migration_name = '{migration_name}';"
        ).fetchone()
        is not None
    )
