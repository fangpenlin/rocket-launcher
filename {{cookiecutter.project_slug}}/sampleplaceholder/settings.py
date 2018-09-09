# -*- coding: utf-8 -*-
import os

from .utils import asbool

DEFAULT_SECRET_KEY = "DEFAULT_SECRET_KEY"


class Config(object):
    """Base configuration."""
    SECRET_KEY = os.environ.get("SECRET_KEY", DEFAULT_SECRET_KEY)
    BCRYPT_LOG_ROUNDS = 13
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = "simple"  # Can be "memcached", "redis", etc.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "postgresql://localhost/sampleplaceholder"
    )

    # Flask-Mail configs
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.sendgrid.net")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", "2525"))
    MAIL_USERNAME = os.environ.get("SENDGRID_USERNAME")
    MAIL_PASSWORD = os.environ.get("SENDGRID_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")
    MAIL_USE_TLS = asbool(os.environ.get("MAIL_USE_TLS", "true"))
    MAIL_DEBUG = asbool(os.environ.get("MAIL_DEBUG", "false"))

    # Flask-Security configs
    SECURITY_REGISTERABLE = asbool(os.environ.get("SECURITY_REGISTERABLE", "true"))
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT", SECRET_KEY)
    SECURITY_EMAIL_SENDER = os.environ.get("SECURITY_EMAIL_SENDER", MAIL_DEFAULT_SENDER)


class ProdConfig(Config):
    """Production configuration."""
    ENV = "prod"
    DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar


class DevConfig(Config):
    """Development configuration."""
    ENV = "dev"
    DEBUG = True
    DEBUG_TB_ENABLED = True
    CACHE_TYPE = "simple"  # Can be "memcached", "redis", etc.


class TestConfig(Config):
    """Test configuration."""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "postgresql://localhost/sampleplaceholder_test"
    )

    BCRYPT_LOG_ROUNDS = 4  # For faster tests; needs at least 4 to avoid "ValueError: Invalid rounds"
    WTF_CSRF_ENABLED = False  # Allows form testing
    # xxx:
    # https://github.com/jarus/flask-testing/issues/21
    PRESERVE_CONTEXT_ON_EXCEPTION = False
