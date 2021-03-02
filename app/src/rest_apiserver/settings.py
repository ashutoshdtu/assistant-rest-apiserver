"""
    SETTINGS
    ~~~~~~~~~~~~~~~~~

    Settings file for rest_apiserver.

    :license: GPL-3.0, see LICENSE for more details.
"""
import logging
logger = logging.getLogger(__name__)
logger.info("Loaded " + __name__)

import os
from rest_apiserver.models import *

API_VERSION = 'v1'
DEBUG = True

SWAGGER_INFO = {
    'title': 'REST API Server',
    'version': '0.1.0',
    'description': 'REST APIs for Cloud Provisioning Assistant',
    'termsOfService': 'For demo purposes only. Use at your own risk',
    'contact': {
        'name': 'Ashutosh Mishra',
        'url': 'https://ashutoshmishra.net'
    },
    'license': {
        'name': 'GPL-3.0',
        'url': 'https://github.com/ashutoshdtu/assistant-rest-apiserver/-/raw/master/LICENSE',
    },
    'schemes': ['https','http'],
}

BASE_DIR=os.path.dirname(os.path.abspath(__file__))
DEFAULT_CONFIG_FILE = os.path.join(BASE_DIR, 'settings.ini')
LOGGER_CONFIG = os.path.join(BASE_DIR, 'logger.conf')
# CONFIG_FILE = ""

# All APIs
DOMAIN = {
    'users': users,
    'roles': roles,
    'provisionRequests': provisionRequests,
    'extensionRequests': extensionRequests,
    'quotas': quotas,
    'notifications': notifications,
    'templates': templates,
    'estimatedBills': estimatedBills,
    'instancePricing': instancePricing,
    'diskPricing': diskPricing
}

X_DOMAINS = ['http://localhost:8000']  # The domain where Swagger UI is running
X_HEADERS = ['Content-Type', 'If-Match', 'Authorization']  # Needed for the "Try it out" buttons