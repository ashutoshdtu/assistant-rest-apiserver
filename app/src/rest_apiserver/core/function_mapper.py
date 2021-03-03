"""
    rest_apiserver.core.function_mapper
    ~~~~~~~~~~~~~~~~~

    Class to build a dict of functions using decorators. 

    :license: GPL-3.0, see LICENSE for more details.
"""

import logging
logger = logging.getLogger(__name__)
logger.debug("Loaded " + __name__)

class FunctionMapper():
    def __init__(self):
        self.routes = {}

    def add(self, route_str):
        def decorator(f):
            self.routes[route_str] = f
            return f

        return decorator

    def get(self, path):
        view_function = self.routes.get(path)
        if view_function:
            return view_function
        else:
            raise ValueError('Route "{}"" has not been registered'.format(path))

    def _routes(self):
        return self.routes.keys()
