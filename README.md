<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/SpaceShaman/SQLift/refs/heads/master/assets/logo-light.png">
  <img src="https://raw.githubusercontent.com/SpaceShaman/SQLift/refs/heads/master/assets/logo-dark.png" alt="SQLift">
</picture>

[![GitHub License](https://img.shields.io/github/license/SpaceShaman/SQLift)](https://github.com/SpaceShaman/SQLift?tab=MIT-1-ov-file)
[![Tests](https://img.shields.io/github/actions/workflow/status/SpaceShaman/SQLift/release.yml?label=tests)](https://app.codecov.io/github/SpaceShaman/SQLift)
[![Codecov](https://img.shields.io/codecov/c/github/SpaceShaman/SQLift)](https://app.codecov.io/github/SpaceShaman/SQLift)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/SQLift)](https://pypi.org/project/SQLift)
[![PyPI - Version](https://img.shields.io/pypi/v/SQLift)](https://pypi.org/project/SQLift)
[![Code style: black](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)
[![Linting: Ruff](https://img.shields.io/badge/linting-Ruff-black?logo=ruff&logoColor=black)](https://github.com/astral-sh/ruff)
[![SQLite](https://img.shields.io/badge/technology-SQLite-blue?logo=sqlite&logoColor=blue)](https://www.sqlite.org)
[![PostgreSQL](https://img.shields.io/badge/technology-PostgreSQL-blue?logo=postgresql&logoColor=blue)](https://www.postgresql.org)
[![Pytest](https://img.shields.io/badge/testing-Pytest-red?logo=pytest&logoColor=red)](https://docs.pytest.org/)

SQLift is a simple CLI migration tool for SQL databases. It is designed to be easy to use and now supports [SQLite](https://www.sqlite.org) and [PostgreSQL](https://www.postgresql.org) databases.

## Installation

You can install SQLift using pip:

```bash
pip install SQLift
```

By default, SQLift uses [SQLite](https://www.sqlite.org) as the database. If you want to use [PostgreSQL](https://www.postgresql.org), you need to install the appropriate database driver.
You can do this using the following command:

```bash
pip install SQLift[postgres]
```

## Usage

First you need to create a 'migrations' directory where you will store your migration files.
Migrations are simple SQL files that contain the SQL commands to be executed for `up` and `down` migrations like below.
This file needs two sections, one for the `up` migration and one for the `down` migration, separated by `--DOWN`.

### Example migration file

```sql
migrations/001_create_table.sql 
--UP
CREATE TABLE IF NOT EXISTS test (
    id INTEGER PRIMARY KEY
);

--DOWN
DROP TABLE IF EXISTS test;
```

You can find more examples of migration files in the [migrations](https://github.com/SpaceShaman/SQLift/tree/master/migrations) directory of this repository.

After you have created your migration files, you can run the following command to apply the migrations to your database. (It is recommended to start the migration files with a number to keep them in order)

```bash
sqlift up
```

This will apply all the migrations that have not been applied yet. If you want migrate to a specific version, you can pass the version as an argument.

```bash
sqlift up 001_create_table
```

To rollback all migrations, you can run the following command.

```bash
sqlift down
```

To rollback to a specific version, you can pass the version

```bash
sqlift down 001_create_table
```

You can also select specific path for migrations directory

```bash
sqlift up --path /path/to/migrations
```

## Configuration

SQLift uses environment variables to configure the database connection. You can set the following environment variables to configure the database connection.

```env
DB_URL=postgresql://user:password@localhost:5432/database # PostgreSQL
DB_URL=sqlite:///path/to/database.db                      # SQLite
```

If you don't set the `DB_URL` environment variable, SQLift will default to using [SQLite](https://www.sqlite.org) with a database file named `db.sqlite` in the current directory.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.
I would like to keep the library to be safe as possible, so i would appreciate if you cover any new feature with tests to maintain 100% coverage.

### Install in a development environment

1. First, clone the repository:

    ```bash
    git clone git@github.com:SpaceShaman/SQLift.git
    ```

2. Install poetry if you don't have, here you can find the [instructions](https://python-poetry.org/docs/#installing-with-the-official-installer)

3. Create a virtual environment and install the dependencies:

    ```bash
    cd SQLift
    poetry install --no-root
    ```

4. Activate the virtual environment:

    ```bash
    poetry shell
    ```

### Run tests

First, you need to run databases and you can do it simply with docker-compose:

```bash
docker compose up -d
```

Then you can run the tests with pytest:

```bash
pytest
```

You can also run the tests with coverage:

```bash
pytest --cov=sqlift
```

### Database clients

If you want to add support for a new database, you need to create a new client class that is consistent with the `Client` protocol class from [sqlift.clients](https://github.com/SpaceShaman/SQLift/blob/master/sqlift/clients.py) and implement the `execute` method. Look at the `SQLiteClient` and `PostgreSQLClient` classes for reference.
