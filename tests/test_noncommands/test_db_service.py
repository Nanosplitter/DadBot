import pytest
from noncommands.db_service import get_db_noncommands

def test_get_db_noncommands():
    db = get_db_noncommands()
    assert db is not None
    assert db.database == "test_db"
    assert db.user == "test_user"
    assert db.password == "test_password"
    assert db.host == "test_host"
    assert db.port == 3306
