import pytest

from {{cookiecutter.project_slug}}.blueprints.public.forms import LoginForm
from {{cookiecutter.project_slug}}.blueprints.public.forms import RegisterForm


@pytest.mark.usefixtures("db")
class TestRegisterForm:
    def test_validate_email_already_registered(self, user):
        form = RegisterForm(
            email=user.email, password="example", confirm="example", agree_terms="1",
        )

        assert not form.validate()
        assert "Email already registered" in form.email.errors

    @pytest.mark.parametrize(
        "invalid_password", ["Example", "eXaMpLe", "EXAMPLE", "e", "example1", "foobar"]
    )
    def test_validate_password_do_not_match(self, invalid_password):
        form = RegisterForm(
            email="foo@bar.com",
            password="example",
            confirm=invalid_password,
            agree_terms="1",
        )

        assert not form.validate()
        assert "Passwords must match" in form.confirm.errors

    def test_validate_terms_not_agreed(self):
        form = RegisterForm(email="foo@bar.com", password="example", confirm="example")

        assert not form.validate()
        assert (
            "You need to agree to Terms of Service to register"
            in form.agree_terms.errors
        )

    def test_validate_success(self, user):
        form = RegisterForm(
            email="new@test.test",
            password="example",
            confirm="example",
            agree_terms="1",
        )
        assert form.validate()


@pytest.mark.usefixtures("db")
class TestLoginForm:
    def test_validate_success(self, user, default_password):
        form = LoginForm(email=user.email, password=default_password)
        assert form.validate()
        assert form.user == user

    def test_validate_unknown_email(self, user, default_password):
        form = LoginForm(email="unknown@gmail.com", password=default_password)
        assert not form.validate()
        assert "Invalid email or password" in form.email.errors
        assert form.user is None

    def test_validate_invalid_password(self, user, default_password):
        form = LoginForm(email=user.email, password=default_password + "1")
        assert not form.validate()
        assert "Invalid email or password" in form.email.errors

    def test_validate_inactive_user(self, inactive_user, default_password):
        form = LoginForm(email=inactive_user.email, password=default_password)
        assert not form.validate()
        assert "User not activated" in form.email.errors
