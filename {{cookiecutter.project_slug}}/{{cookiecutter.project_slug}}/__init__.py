# -*- coding: utf-8 -*-
from flask.helpers import get_debug_flag

from {{cookiecutter.project_slug}}.app import create_app
from {{cookiecutter.project_slug}}.settings import DevConfig
from {{cookiecutter.project_slug}}.settings import ProdConfig

CONFIG = DevConfig if get_debug_flag() else ProdConfig

app = create_app(CONFIG)
