import datetime

from flask_login import UserMixin
from sqlalchemy import Column
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID

from ..extensions import bcrypt
from ..extensions import db
from .base import Model


class User(UserMixin, Model):
    __tablename__ = "users"
    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    email = Column(db.String(80), unique=True, nullable=False)
    #: The hashed password
    password = Column(db.LargeBinary(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    is_active = Column(db.Boolean(), default=True, server_default="f", nullable=False)
    is_admin = Column(db.Boolean(), default=False, server_default="f", nullable=False)
    # last time we sent reset password email
    sent_reset_password_at = Column(db.DateTime, nullable=True)
    # last time we reset password via reset link
    reset_password_at = Column(db.DateTime, nullable=True)

    def __init__(self, email, password=None, **kwargs):
        """Create instance."""
        db.Model.__init__(self, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    def __repr__(self):
        return f"<User({self.email!r})>"
