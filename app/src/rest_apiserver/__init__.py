# -*- coding: utf-8 -*-

"""
    rest_apiserver
    ~~~~~~~~~~~~
    REST API Server for Cloud Provisioning Assistant.
    :license: GPL-3.0, see LICENSE for more details.
"""

import os
BASE_DIR=os.path.dirname(os.path.abspath(__file__))
# DEFAULT_CONFIG_FILE = os.path.join(BASE_DIR, 'settings.ini')
LOGGER_CONFIG = os.path.join(BASE_DIR, 'logger.conf')
# STATIC_DIR = os.path.join(os.path.dirname(BASE_DIR), 'docs')
SETTINGS_FILE = os.path.join(BASE_DIR, 'settings.py')


__author__ = """Ashutosh Mishra"""
__email__ = 'ashutoshdtu@gmail.com'
__version__ = '0.1.0'


import logging
import logging.config
print ("Logger config location", LOGGER_CONFIG)
logging.config.fileConfig(LOGGER_CONFIG)
logger = logging.getLogger(__name__)
logger.debug("Loaded " + __name__)

from .server import Server
app = Server(__name__, settings=SETTINGS_FILE)
app.config['SWAGGER_HOST'] = app.config['HOST_NAME']

# from . import core
# from . import rpc
from . import controllers
