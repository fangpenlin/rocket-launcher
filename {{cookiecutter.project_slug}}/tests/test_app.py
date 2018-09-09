import pytest
from flask import url_for


def test_default_security_token_in_prod(testapp):
    testapp.app.debug = False
    resp = testapp.get(url_for("public.home"), status=500)
    assert "SECRET_KEY cannot be default value" in resp


def test_short_security_token_in_prod(testapp):
    testapp.app.debug = False
    testapp.app.config["SECRET_KEY"] = "SHORT"
    resp = testapp.get(url_for("public.home"), status=500)
    assert "SECRET_KEY too short" in resp


def test_security_token_pass_in_prod(testapp):
    testapp.app.debug = False
    testapp.app.config["SECRET_KEY"] = "a" * 32
    testapp.get(url_for("public.home"), status=200)


def test_raise_error(testapp):
    with pytest.raises(RuntimeError):
        testapp.get(url_for("public.raise_error"))
