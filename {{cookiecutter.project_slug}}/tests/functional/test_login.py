from flask import url_for


def test_can_log_in_returns_200(testapp, user, default_password):
    res = testapp.get(url_for("public.login"))
    form = res.form
    form["email"] = user.email
    form["password"] = default_password
    res = form.submit().follow()
    assert res.status_code == 200


def test_can_login_with_different_email_case_in_returns_200(
    db, testapp, user_factory, default_password
):
    user_factory(email="myemail@gmail.com")
    res = testapp.get(url_for("public.login"))
    form = res.form
    form["email"] = "MyEmail@Gmail.com"
    form["password"] = default_password
    res = form.submit().follow()
    assert res.status_code == 200


def test_sees_alert_on_logout(testapp, user, default_password):
    res = testapp.get(url_for("public.login"))
    form = res.form
    form["email"] = user.email
    form["password"] = default_password
    res = form.submit().follow()
    res = testapp.get(url_for("public.logout")).follow()
    assert "You are logged out." in res


def test_sees_error_message_if_password_is_incorrect(testapp, user, default_password):
    res = testapp.get(url_for("public.login"))
    form = res.form
    form["email"] = user.email
    form["password"] = default_password + "1"
    res = form.submit()
    assert "Invalid email or password" in res


def test_sees_error_message_if_username_doesnt_exist(testapp, user, default_password):
    res = testapp.get(url_for("public.login"))
    form = res.form
    form["email"] = "unknown@gmail.com"
    form["password"] = default_password
    res = form.submit()
    assert "Invalid email or password" in res
