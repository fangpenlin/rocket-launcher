import pytest
from flask_webtest import TestApp
from sampleplaceholder.app import create_app
from sampleplaceholder.extensions import db as _db
from sampleplaceholder.settings import TestConfig


@pytest.fixture
def app():
    """An application for the tests."""
    _app = create_app(TestConfig)
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture
def testapp(app, db):
    """A Webtest app."""
    return TestApp(app, db=db)


@pytest.fixture
def db(app):
    """A database for the tests."""
    _db.app = app
    with app.app_context():
        _db.create_all()

    yield _db

    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()
