# -*- coding: utf-8 -*-
"""Create an application instance."""
from flask.helpers import get_debug_flag
from sampleplaceholder.app import create_app
from sampleplaceholder.settings import DevConfig
from sampleplaceholder.settings import ProdConfig

CONFIG = DevConfig if get_debug_flag() else ProdConfig

app = create_app(CONFIG)
