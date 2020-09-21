from flask import url_for

from {{cookiecutter.project_slug}}.models.accounts import User


def test_register(testapp):
    res = testapp.get(url_for("public.register"))
    form = res.form
    form["email"] = "foo@bar.com"
    form["password"] = "secret"
    form["confirm"] = "secret"
    form["agree_terms"] = "1"
    res = form.submit().follow()
    assert res.status_code == 200
    user = User.query.filter_by(email="foo@bar.com").first()
    assert user is not None
