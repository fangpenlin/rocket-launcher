import pytest
from flask_webtest import TestApp

from {{cookiecutter.project_slug}}.app import create_app
from {{cookiecutter.project_slug}}.extensions import db as _db
from {{cookiecutter.project_slug}}.settings import TestConfig


def pytest_sessionstart(session):
    _app = create_app(TestConfig)
    ctx = _app.test_request_context()
    ctx.push()

    with _app.app_context():
        _db.engine.execute('''
        CREATE EXTENSION IF NOT EXISTS pgcrypto
        ''')

    ctx.pop()


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
