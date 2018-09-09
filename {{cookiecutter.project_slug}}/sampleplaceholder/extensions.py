# -*- coding: utf-8 -*-
"""
Extensions module. Each extension is initialized in the app factory located
in app.py.
"""
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail
from flask_migrate import Migrate
from flask_security import Security
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

csrf_protect = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()
debug_toolbar = DebugToolbarExtension()
security = Security()
mail = Mail()
