# -*- coding: utf-8 -*-
"""Public section, including homepage and other public pages."""

from flask import Blueprint
from flask import abort
from flask import current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import url_for

blueprint = Blueprint("public", __name__, static_folder="../../static")


@blueprint.route("/", methods=["GET"])
def home():
    """Home page."""
    return render_template("public/home.html")


@blueprint.route("/terms-of-service/")
def terms():
    """TOS page."""
    return render_template("public/terms.html")


@blueprint.route("/__raise_error__/")
def raise_error():
    # for testing bugsnag
    raise RuntimeError("failed")


@blueprint.route("/robots.txt")
def static_from_root():
    return send_from_directory(current_app.static_folder, request.path[1:])
