"""
    rest_apiserver.core
    ~~~~~~~~~~~~~~~~~

    The core module for rest_apiserver. 

    :license: GPL-3.0, see LICENSE for more details.
"""

import logging
logger = logging.getLogger(__name__)
logger.debug("Loaded " + __name__)

# from ..core.function_mapper import FunctionMapper 
# mongo_pipelines = FunctionMapper()

from .function_mapper import *
from .utils import *
# from .redis_connector import *
