import os
import sqlite3

import pytest


@pytest.fixture
def cursor():
    with sqlite3.connect("db.sqlite") as connection:
        yield connection.cursor()
    if os.path.exists("db.sqlite"):
        os.remove("db.sqlite")
