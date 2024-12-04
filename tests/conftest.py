import os

import pytest

from sqlift.clients import get_client


@pytest.fixture(
    params=[
        "sqlite:///db.sqlite",
        "postgresql://user:password@localhost/db",
    ]
)
def client(request):
    os.environ["DB_URL"] = request.param
    yield get_client()
    if os.path.exists("db.sqlite"):
        os.remove("db.sqlite")
