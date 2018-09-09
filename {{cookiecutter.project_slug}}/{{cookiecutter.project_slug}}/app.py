# -*- coding: utf-8 -*-
from bugsnag.flask import handle_exceptions
from flask import Flask
from flask import Response
from flask import abort
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_security import SQLAlchemySessionUserDatastore

from . import commands
from .blueprints import public
from .extensions import csrf_protect
from .extensions import db
from .extensions import debug_toolbar
from .extensions import mail
from .extensions import migrate
from .extensions import security
from .models.accounts import Role
from .models.accounts import User
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
    register_secret_key_check(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""

    db.init_app(app)
    csrf_protect.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    security.init_app(app, SQLAlchemySessionUserDatastore(db.session, User, Role))
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
    return None
