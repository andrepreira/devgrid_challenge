from sqlalchemy.orm import Session

from app.api.v1.endpoints import get_db


def test_get_db():
    with next(get_db()) as db:
        assert isinstance(db, Session)
    assert db.is_active == True
