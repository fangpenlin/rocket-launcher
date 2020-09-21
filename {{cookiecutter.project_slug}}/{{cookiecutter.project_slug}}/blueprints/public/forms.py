from flask_wtf import FlaskForm
from wtforms import BooleanField
from wtforms import PasswordField
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms.validators import Email
from wtforms.validators import EqualTo
from wtforms.validators import Length

from ...models.accounts import User


class LoginForm(FlaskForm):
    """Login form."""

    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember me", validators=[])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False

        self.user = User.query.filter(User.email.ilike(self.email.data)).first()
        if not self.user or not self.user.check_password(self.password.data):
            self.email.errors.append("Invalid email or password")
            return False

        if not self.user.is_active:
            self.email.errors.append("User not activated")
            return False
        return True


class RegisterForm(FlaskForm):
    """Register form."""

    email = StringField(
        "Email", validators=[DataRequired(), Email(), Length(min=6, max=40)],
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=40)],
    )
    confirm = PasswordField(
        "Verify password",
        [DataRequired(), EqualTo("password", message="Passwords must match")],
    )
    agree_terms = BooleanField(
        "Agree terms",
        validators=[
            DataRequired(message="You need to agree to Terms of Service to register",)
        ],
    )

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter(User.email.ilike(self.email.data)).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        return True


class ForgotPasswordForm(FlaskForm):
    """Forgot password form."""

    email = StringField("Email", validators=[DataRequired(), Email()])

    def validate(self):
        """Validate the form."""
        initial_validation = super(ForgotPasswordForm, self).validate()
        if not initial_validation:
            return False
        return True


class ResetPasswordForm(FlaskForm):
    """Reset password form."""

    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=40)],
    )
    confirm = PasswordField(
        "Verify password",
        [DataRequired(), EqualTo("password", message="Passwords must match")],
    )
