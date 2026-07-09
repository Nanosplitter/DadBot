import pytest
from services.db_service import get_db

def test_get_db():
    db = get_db()
    assert db is not None
    assert db.database == "test_db"
    assert db.user == "test_user"
    assert db.password == "test_password"
    assert db.host == "test_host"
    assert db.port == 3306
