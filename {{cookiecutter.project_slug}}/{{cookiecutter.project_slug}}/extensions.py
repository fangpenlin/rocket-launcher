"""
Extensions module. Each extension is initialized in the app factory located
in app.py.
"""
from flask_bcrypt import Bcrypt
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_principal import Principal
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

csrf_protect = CSRFProtect()
bcrypt = Bcrypt()
db = SQLAlchemy()
migrate = Migrate()
debug_toolbar = DebugToolbarExtension()
login_manager = LoginManager()
principal = Principal()
mail = Mail()
