"""Database module, including the SQLAlchemy database object and DB-related
utilities."""
from ..extensions import db


class Model(db.Model):
    """Base model class that includes CRUD convenience methods."""

    __abstract__ = True
