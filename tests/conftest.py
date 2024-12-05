import os

import pytest

from sqlift.clients import get_client


@pytest.fixture(
    params=[
        "sqlite:///db.sqlite",
        "postgresql://postgres:password@localhost/postgres",
    ]
)
def client(request):
    os.environ["DB_URL"] = request.param
    client = get_client()
    yield client
    _clean_db(client)


def _clean_db(client):
    if os.path.exists("db.sqlite"):
        os.remove("db.sqlite")
    if os.getenv("DB_URL", "").startswith("postgresql"):
        client.execute("DROP TABLE IF EXISTS test;")
        client.execute("DROP TABLE IF EXISTS migrations;")
