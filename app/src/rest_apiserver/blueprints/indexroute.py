"""
    rest_apiserver.blueprints.indexroute
    ~~~~~~~~~~~~~~~~~

    Flask blueprint for the root API route listing all the available sunbroutes.

    :license: GPL-3.0, see LICENSE for more details.
"""

import logging
logger = logging.getLogger(__name__)
logger.debug("Loaded " + __name__)

import os
import operator

from rest_apiserver.core.utils import list_routes, get_app_config_as_dict, toJSON

from flask import Blueprint, jsonify, Response, make_response, request, \
    current_app as app

index_bp = Blueprint('index', __name__)

@index_bp.route('/', methods=['GET'])
def index():
    response = {
        "_links": {
            "all": list_routes()
        },
        "_meta": {
            "build": {
                "href": os.environ.get('CI_BUILD_LINK', '-')
            }
        }
    }
    return jsonify(response)
