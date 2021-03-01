# -*- coding: utf-8 -*-

"""
    rest_apiserver.server
    ~~~~~~~~~~~~
    This module implements the central WSGI application object as a Python Eve
    subclass.
    :license: GPL-3.0, see LICENSE for more details.
"""

import logging
logger = logging.getLogger(__name__)
logger.debug("Loaded " + __name__)

import os

from events import Events

from eve import Eve
# from eve_swagger import swagger, add_documentation
from eve_swagger import get_swagger_blueprint, add_documentation
from eve.io.mongo import Mongo, Validator, GridFSMediaStorage

# from .rpc import methods
from .blueprints import *

class Server(Eve, Events):
    
    # methods = methods
    
    def __init__(
        self,
        import_name=__package__,
        settings="settings.py",
        validator=Validator,
        data=Mongo,
        auth=None,
        redis=None,
        url_converters=None,
        json_encoder=None,
        media=GridFSMediaStorage,
        configs=[],
        env_prefix="APP_",
        **kwargs
    ):
        """ Server main WSGI app is implemented as a Eve subclass. Since we want
        to be able to launch our API by simply invoking Eve's run() method,
        we need to enhance our super-class a little bit.
        """

        super(Server, self).__init__(import_name, **kwargs)
        
        self.load_server_config(configs, env_prefix)
        self.logger = logger
        self.load_blueprints()
        

    def load_server_config(self, configs, env_prefix):
        """
        Loads the config from environment and settings file.
        
        Order: 
        settings.py -> settings.ini -> [configs] -> 
        APP_* (env) -> CONFIG_FILE
        """
        # 1. Loads from settings.ini [default settings]
        logger.debug("Loading " + str(self.config['DEFAULT_CONFIG_FILE']) + " [default settings]...")
        self.config.from_pyfile(self.config['DEFAULT_CONFIG_FILE']) 
        
        # 2. Loads user provided settings file
        for config_file in configs:
            if os.path.isfile(config_file):
                logger.debug("Loading "+str(config_file)+"...")
                self.config.from_pyfile(config_file)
        
        # 3. Finally loads from Environment Variables
        for a in os.environ: 
            if(a.startswith(env_prefix)):
                self.config[a[len(env_prefix):]] = os.getenv(a)
        
        # 4. Loads user provided settings file
        if 'CONFIG_FILE' in self.config: 
            logger.debug("Loading " + self.config['CONFIG_FILE'] + "...")
            self.config.from_pyfile(self.config['CONFIG_FILE'])
        

        
    def load_blueprints(self):
        if self.config["ENABLE_SWAGGER_ROUTES"]:
            logger.debug("Enabling swagger routes...")
            swagger = get_swagger_blueprint()
            self.register_blueprint(swagger)
        if self.config["ENABLE_CONFIG_ROUTES"]:
            logger.debug("Enabling config routes...")
            self.register_blueprint(config_bp)
        if self.config["ENABLE_HEALTH_ROUTES"]:
            logger.debug("Enabling health routes...")
            self.register_blueprint(health_bp)
        # if self.config["ENABLE_JSONRPC_ROUTES"]:
        #     logger.debug("Enabling RPC routes...")
        #     rpc_route = '/' + self.config["API_VERSION"] + '/' + self.config["RPC_BASE_ROUTE"] + '/' + self.config["RPC_ROUTE_NAME"]
        #     self.add_url_rule(
        #         rpc_route, "call_rpc", view_func=call_rpc, methods=["POST", "OPTIONS"]
        #     )
        #     self.add_url_rule(
        #         rpc_route, "list_rpc", view_func=list_rpc, methods=["GET", "OPTIONS"]
        #     )
        if self.config["ENABLE_INDEX_ROUTES"]:
            logger.debug("Enabling index routes...")
            self.register_blueprint(index_bp)
        
