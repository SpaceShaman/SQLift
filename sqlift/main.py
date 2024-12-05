from pathlib import Path
from typing import Optional

from rich import print
from typer import Argument, Typer
from typing_extensions import Annotated

from .clients import Client, get_client

app = Typer()


@app.command()
def up(target_migration: Annotated[Optional[str], Argument()] = None) -> None:
    """Apply migrations up to the target migration or all if no target is provided."""
    client = get_client()
    _create_migrations_table_if_not_exists(client)
    for migration_name in _get_migration_names(target_migration):
        _apply_migration(client, migration_name)
    if target_migration:
        print(
            f"[bold green]All migrations up to {target_migration} applied successfully[/bold green] :thumbs_up:"
        )
    else:
        print(
            "[bold green]All migrations applied successfully[/bold green] :thumbs_up:"
        )


@app.command()
def down(target_migration: Annotated[Optional[str], Argument()] = None) -> None:
    """Revert migrations down to the target migration or all if no target is provided."""
    client = get_client()
    _create_migrations_table_if_not_exists(client)
    for migration_name in _get_migration_names(target_migration, reverse=True):
        _revert_migration(client, migration_name)
    if target_migration:
        print(
            f"[bold green]All migrations down to {target_migration} reverted successfully[/bold green] :thumbs_up:"
        )
    else:
        print(
            "[bold green]All migrations reverted successfully[/bold green] :thumbs_up:"
        )


def _apply_migration(client: Client, migration_name: str) -> None:
    if _is_migration_recorded(client, migration_name):
        return
    client.execute(_get_sql_up_command(migration_name))
    _record_migration(client, migration_name)
    print(f"[green]- {migration_name}[/green] applied successfully")


def _revert_migration(client: Client, migration_name: str) -> None:
    if not _is_migration_recorded(client, migration_name):
        return
    client.execute(_get_sql_down_command(migration_name))
    _delete_migration_record(client, migration_name)
    print(f"[red]- {migration_name}[/red] reverted successfully")


def _get_migration_names(
    target_migration: str | None, reverse: bool = False
) -> list[str]:
    migration_names = sorted(
        [migration_path.stem for migration_path in Path("migrations").glob("*.sql")],
        reverse=reverse,
    )
    if target_migration:
        return migration_names[: migration_names.index(target_migration) + 1]
    return migration_names


def _get_sql_commands(migration_name: str) -> list[str]:
    return open(f"migrations/{migration_name}.sql").read().split("--DOWN")


def _get_sql_up_command(migration_name: str) -> str:
    return _get_sql_commands(migration_name)[0]


def _get_sql_down_command(migration_name: str) -> str:
    return _get_sql_commands(migration_name)[1]


def _record_migration(client: Client, migration_name: str) -> None:
    client.execute(
        f"INSERT INTO migrations (migration_name) VALUES ('{migration_name}');"
    )


def _delete_migration_record(client: Client, migration_name: str) -> None:
    client.execute(f"DELETE FROM migrations WHERE migration_name = '{migration_name}';")


def _create_migrations_table_if_not_exists(client: Client) -> None:
    client.execute("""
        CREATE TABLE IF NOT EXISTS migrations (
            migration_name TEXT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)


def _is_migration_recorded(client: Client, migration_name: str) -> bool:
    return (
        client.execute(
            f"SELECT * FROM migrations WHERE migration_name = '{migration_name}';"
        ).fetchone()
        is not None
    )
