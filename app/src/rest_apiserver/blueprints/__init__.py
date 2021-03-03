"""
    rest_apiserver.blueprints
    ~~~~~~~~~~~~~~~~~

    Flask blueprints.

    :license: GPL-3.0, see LICENSE for more details.
"""

import logging
logger = logging.getLogger(__name__)
logger.debug("Loaded " + __name__)

from .config import *
from .healthz import *
from .indexroute import *
# from .jsonrpc import *
