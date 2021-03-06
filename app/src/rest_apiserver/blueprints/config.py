"""
    rest_apiserver.blueprints.config
    ~~~~~~~~~~~~~~~~~

    Flask blueprint for config API routes.

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

config_bp = Blueprint('config', __name__)

@config_bp.route('/config', methods=['GET'])
def config():
    response = get_app_config_as_dict()
    return Response(toJSON(response), 200,
        mimetype='application/json')

@config_bp.route('/info', methods=['GET'])
def get_info():
    response = {
        "name": app.config["NAME"],
        "description": app.config["DESCRIPTION"],
        "version": app.config["VERSION"],
        "build": {
            "href": os.environ.get('CI_BUILD_LINK', '-')
        },
        "repo": {
            "name": os.environ.get('CI_REPO_NAME', '-'),
            "href": os.environ.get('CI_REPO_LINK', '-')
        },
        "commit": {
            "href": os.environ.get('CI_COMMIT_LINK', '-'),
            "author": os.environ.get('CI_COMMIT_AUTHOR_EMAIL', '-'),
        }
    }
    return jsonify(response)
