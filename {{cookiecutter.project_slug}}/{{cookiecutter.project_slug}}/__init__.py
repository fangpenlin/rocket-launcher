from flask.helpers import get_debug_flag

from .app import create_app
from .settings import DevConfig
from .settings import ProdConfig

CONFIG = DevConfig if get_debug_flag() else ProdConfig

app = create_app(CONFIG)
