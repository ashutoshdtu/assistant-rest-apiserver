"""
    rest_apiserver.controllers
    ~~~~~~~~~~~~~~~~~

    Custom flask routes. 

    :license: GPL-3.0, see LICENSE for more details.
"""

import logging
logger = logging.getLogger(__name__)
logger.info("Loaded " + __name__)

from . import reviews