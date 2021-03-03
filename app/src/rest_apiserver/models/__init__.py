"""
    rest_apiserver.models
    ~~~~~~~~~~~~~~~~~

    MongoDB schemas for all REST APIs.

    This exports all API schemas:

    - rest_apiserver.models.aws_pricing exports schema for various AWS Resource Pricing APIs. 
    - rest_apiserver.models.notifications exports schema for Notifications APIs. 
    - rest_apiserver.models.provision_requests exports schema for Provision Request and
      Extension Request APIs. 
    - rest_apiserver.models.templates exports schema for resource templates APIs. 
    - rest_apiserver.models.users exports schema for Users, Roles, Quotas and Estimated Bills APIs.

    :license: GPL-3.0, see LICENSE for more details.
"""

import logging
logger = logging.getLogger(__name__)
logger.info("Loaded " + __name__)

from ..models.users import users, roles, estimatedBills, quotas
from ..models.provision_requests import provisionRequests, extensionRequests
from ..models.notifications import notifications
from ..models.templates import templates
from ..models.aws_pricing import instancePricing, diskPricing