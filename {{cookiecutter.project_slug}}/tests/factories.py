from factory import post_generation
from factory import Sequence
from factory.alchemy import SQLAlchemyModelFactory

from {{cookiecutter.project_slug}}.extensions import db
from {{cookiecutter.project_slug}}.models.accounts import User

USER_DEFAULT_PASSWORD = "myprecious"


class BaseFactory(SQLAlchemyModelFactory):
    """Base factory."""

    class Meta:
        """Factory configuration."""

        abstract = True
        sqlalchemy_session = db.session


class UserFactory(BaseFactory):
    class Meta:
        model = User
        sqlalchemy_session_persistence = "commit"

    email = Sequence(lambda n: "user{0}@example.com".format(n))
    # Notice: these will be populated by column's default values, but it seems like if we want the pytest-factoryboy
    #         value overwriting to work, we will need to define them here
    is_active = True
    is_admin = False

    # Notice: PostGenerationMethodCall is easier to use, but as pytest-factoryboy doesn't support it, so that
    #         we have to use post generation hook here
    @post_generation
    def init_password(obj, create, extracted, **kwargs):
        obj.set_password(extracted or USER_DEFAULT_PASSWORD)
