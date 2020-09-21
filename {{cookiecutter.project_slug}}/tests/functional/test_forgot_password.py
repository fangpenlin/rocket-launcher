import datetime
import re

import jwt
from flask import url_for
from freezegun import freeze_time

from {{cookiecutter.project_slug}}.extensions import mail


def test_forgot_password(testapp, user):
    testapp.app.config["FORGOT_PASSWORD_COOLDOWN_TIME_SECONDS"] = 60 * 10
    testapp.app.config["RESET_PASSWORD_LINK_VALID_SECONDS"] = 123

    res = testapp.get(url_for("public.forgot_password"))
    form = res.form
    form["email"] = user.email
    with mail.record_messages() as outbox:
        res = form.submit()
        assert len(outbox) == 1
        match = re.search("reset-password\\?token=([0-9a-zA-Z.\\-_]+)", outbox[0].body)
        raw_token = match.group(1)
        token = jwt.decode(
            raw_token, key=testapp.app.config["SECRET_KEY"], algorithms=["HS256"],
        )
        user_id = token["user_id"]
        expires_at = datetime.datetime.utcfromtimestamp(token["expires_at"])
        assert user_id == str(user.id)
        assert user.sent_reset_password_at is not None
        assert expires_at == user.sent_reset_password_at + datetime.timedelta(
            seconds=testapp.app.config["RESET_PASSWORD_LINK_VALID_SECONDS"]
        )
    assert "Please check your mailbox for reset password email" in res


def test_forgot_password_cooldown_period(testapp, db, user):
    testapp.app.config["FORGOT_PASSWORD_COOLDOWN_TIME_SECONDS"] = 60 * 10
    testapp.app.config["RESET_PASSWORD_LINK_VALID_SECONDS"] = 123

    now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
    with freeze_time(now):
        user.sent_reset_password_at = now
        db.session.add(user)
        db.session.commit()

    res = testapp.get(url_for("public.forgot_password"))
    form = res.form
    form["email"] = user.email
    with freeze_time(now + datetime.timedelta(seconds=(60 * 10) - 1)):
        res = form.submit().follow()
    assert "We just sent a reset password email to you, please try again later" in res

    with freeze_time(
        now + datetime.timedelta(seconds=60 * 10)
    ), mail.record_messages() as outbox:
        form.submit()
        assert len(outbox) == 1


def test_reset_password_invalid_token(testapp, user):
    res = testapp.get(url_for("public.reset_password", token="foobar")).follow()
    assert "Invalid token" in res


def test_reset_password(testapp, user, default_password):
    now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
    token = jwt.encode(
        dict(
            user_id=str(user.id),
            expires_at=(now + datetime.timedelta(seconds=10)).timestamp(),
            created_at=now.timestamp(),
        ),
        key=testapp.app.config["SECRET_KEY"],
        algorithm="HS256",
    )

    # Ensure reset password link expires
    with freeze_time(now):
        testapp.get(url_for("public.reset_password", token=token), status=200)

    with freeze_time(now + datetime.timedelta(seconds=10)):
        testapp.get(url_for("public.reset_password", token=token), status=200)

    with freeze_time(now + datetime.timedelta(seconds=11)):
        res = testapp.get(url_for("public.reset_password", token=token)).follow()
        assert "Your reset password link has expired" in res

    # Reset password
    new_password = "new" + default_password
    with freeze_time(now + datetime.timedelta(seconds=5)):
        res = testapp.get(url_for("public.reset_password", token=token), status=200)
        form = res.form
        form["password"] = new_password
        form["confirm"] = new_password
        res = form.submit().follow()
        assert "Your password is reset" in res
    assert user.check_password(new_password)

    # See if the link expires after we have reset the password already
    with freeze_time(now):
        res = testapp.get(url_for("public.reset_password", token=token)).follow()
        assert "Your reset password link has expired" in res
