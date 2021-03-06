"""
    rest_apiserver.core.utils
    ~~~~~~~~~~~~~~~~~

    Various utility functions. 

    :license: GPL-3.0, see LICENSE for more details.
"""

import logging
logger = logging.getLogger(__name__)
logger.debug("Loaded " + __name__)

import json
import sys
# if sys.version_info[0] >= 3:
#     from html.parser import HTMLParser
# else:
#     import HTMLParser
from bson import json_util
from bson.son import SON
from bson.objectid import ObjectId
from eve.utils import str_to_date, date_to_rfc1123
from flask import current_app as app
import threading

def bson_to_json(_object):
    return json.loads(json.dumps(_object, default=json_util.default))

def json_to_bson(_object):
    return json_util.loads(json.dumps(_object))

def toJSON(_object):
    return json.dumps(_object, default= lambda o: o.__str__(), 
        sort_keys=True)

def failure_resp(message, code):
    response = {
        "_status": "ERR",
        "_error": {
            "message": message,
            "code": code
        }
    }
    return response

# def unescape(s):
#     h= HTMLParser.HTMLParser()
#     return h.unescape(s)

def get_app_config_as_dict():
    response = {}
    for key in app.config:
        response[key] = app.config[key]
    return response

def list_routes(sort="endpoint", all_methods=False):
    routes = []
    for rule in app.url_map.iter_rules():
        route = {
            "title": rule.endpoint,
            "href": str(rule.rule),
            "methods": sorted(rule.methods)
        }
        routes.append(route)
    return routes

def create_notification(title, description, user):
    """Create a new notification"""
    try:
        notification = {
            "title": title,
            "description": description,
            "user": user
        }
        resp = app.test_client().post('/'+app.config['API_VERSION']+'/notifications/', data=toJSON(notification), content_type='application/json')
        if int(resp.status_code)/100 == 2:
            logger.debug("Notification created successfully")
        else:
            logger.debug("Notification creation failed")
            raise Exception("Notification creation failed")
    except Exception as e:
        # TODO: handle exceptions
        logger.error("Error creating notification: " + str(e), exc_info=1)
        return 1
    return 0

 
# # Execute a function call in thread
# def threaded(call, *args, **kwargs):
#     """Execute ``call(*args, **kwargs)`` in a thread"""
#     thread = threading.Thread(target=call, args=args, kwargs=kwargs)
#     thread.start()
#     return thread

# def is_main_thread_active():
#     return any((i.name == "MainThread") and i.is_alive() for i in threading.enumerate())