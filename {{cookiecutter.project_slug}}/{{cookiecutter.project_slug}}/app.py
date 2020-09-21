from bugsnag.flask import handle_exceptions
from flask import abort
from flask import Flask
from flask import render_template
from flask import Response
from flask_admin import Admin
from flask_login import current_user
from flask_principal import identity_loaded
from flask_principal import UserNeed

from . import commands
from .blueprints import public
from .extensions import bcrypt
from .extensions import csrf_protect
from .extensions import db
from .extensions import debug_toolbar
from .extensions import login_manager
from .extensions import mail
from .extensions import migrate
from .extensions import principal
from .models.accounts import User
from .permissions import admin_role_need
from .settings import DEFAULT_SECRET_KEY
from .settings import ProdConfig


def create_app(config_object=ProdConfig):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    register_template_filters(app)
    register_admin_views(app)
    register_secret_key_check(app)
    register_principals_providers(app)

    login_manager.login_view = "public.login"
    login_manager.login_message_category = "info"
    return app


def register_extensions(app):
    """Register Flask extensions."""

    bcrypt.init_app(app)
    db.init_app(app)
    csrf_protect.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    login_manager.init_app(app)
    principal.init_app(app)
    handle_exceptions(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.views.blueprint)
    return None


def register_errorhandlers(app):
    """Register error handlers."""

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        return render_template("{0}.html".format(error_code)), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {
            "db": db,
            # TODO:
        }

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)
    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.urls)


def register_secret_key_check(app):
    def check_secret_key():
        # ensure SECRET_KEY is set properly
        if not app.debug:
            if app.config["SECRET_KEY"] == DEFAULT_SECRET_KEY:
                abort(Response("SECRET_KEY cannot be default value", 500))
            if len(app.config["SECRET_KEY"]) < 32:
                abort(Response("SECRET_KEY too short", 500))

    app.before_request(check_secret_key)


def register_template_filters(app):
    """Register Flask filters."""
    # TODO: add filters here

    from flask_admin import helpers

    app.jinja_env.globals["h"] = helpers

    return None


def register_admin_views(app):
    import flask_admin.consts
    from .admin import ProtectedAdminIndexView
    from .admin import UserModelView

    url_prefix = app.config["ADMIN_DASHBOARD_PREFIX"]
    admin = Admin(
        app,
        index_view=ProtectedAdminIndexView(url=url_prefix),
        url=url_prefix,
        template_mode="bootstrap3",
    )

    admin.add_view(
        UserModelView(
            User,
            db.session,
            url=f"{url_prefix}/user",
            endpoint="admin.user",
            menu_icon_type=flask_admin.consts.ICON_TYPE_FONT_AWESOME,
            menu_icon_value="user",
        ),
    )


def register_principals_providers(app):
    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        # Set the identity user object
        identity.user = current_user

        if hasattr(current_user, "id"):
            identity.provides.add(UserNeed(current_user.id))

        if current_user.is_authenticated and current_user.is_admin:
            identity.provides.add(admin_role_need)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
