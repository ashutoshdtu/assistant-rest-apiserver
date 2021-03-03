"""
    rest_apiserver.models.provision_requests
    ~~~~~~~~~~~~~~~~~

    Schema for Provision Request and Extension Request APIs. 

    :license: GPL-3.0, see LICENSE for more details.
"""

# API schema for provision requests
provisionRequests = {
    'item_title': 'provisionRequest',

    'resource_methods': ["POST", "GET"],
    'item_methods': ["GET", "PUT", "DELETE"],

    'datasource': {
        'source': 'provisionRequests', 
        'default_sort': [('_created', -1)]
    },

    'schema': {
        'description': {'type': 'string', 'required': False, 'minlength': 0,'maxlength': 1000},
        'expires_by': {'type': 'datetime', 'required': True}, # time when the resource expires
        # 'expires_in_hours': { 'type': 'number', 'max': 100000 },
        'resource_type': {              # the type of resource that needs to be provisioned
            'type': 'string',
            'default': 'KUBERNETES',
            'allowed': ['KUBERNETES'],  # TODO: expand to ['KUBERNETES', 'INSTANCE', 'S3BUCKET']
            'required': True
        },
        'request_type': {               # the type of request: TEMPORARY or PERMANENT
            'type': 'string',
            'default': 'TEMPORARY',
            'allowed': ['TEMPORARY', 'PERMANENT'] 
        },
        'requested_by': {               # Request created by
            'type': 'objectid',
            'data_relation': {
                'resource': 'users',
                'embeddable': True,
            },
            'required': True
        },
        'reviewed_by': {                # Reviewer id
            'type': 'objectid',
            'data_relation': {
                'resource': 'users',
                'embeddable': True,
            }
        },
        'resource_parameters': {'allow_unknown': True},     # TODO: perform proper sanity check
        'resource_template': {          # template yaml to be used
            'type': 'string',
            'default': 'basic-eks-cluster',
            'data_relation': {
                'resource': 'templates',
                'embeddable': True
            },
            'required': True
        },
        'status': {
            'type': 'string',
            'default': 'REQUESTED',
            'allowed': [
                'REQUESTED',        # Request initiated by the developer
                'REVOKED',          # Request revoked by the developer
                'APPROVED',         # Request approved
                'REJECTED',         # Request rejected
                'INITIATED',        # Provisioning initiated
                'DEPLOYED',         # Provisioning succeded
                'FAILED',           # Provisioning failed
                'EXPIRED',          # Expired
                'EXTENDED',         # Expiry date extended
                'PURGE_INITIATED',  # Purge initiated
                'PURGED',           # Purged successfully
                'PURGE_FAILED'      # Purge failed (notify devops recurringly)
            ]
        }
    },
}

# provisions = {

# }

# API schema for extension requests
extensionRequests = {
    'item_title': 'extensionRequest',

    'resource_methods': ["POST", "GET"],
    'item_methods': ["GET", "PUT", "DELETE"],

    'datasource': {
        'source': 'extensionRequests', 
        'default_sort': [('_created', -1)]
    },

    'schema': {
        'reason': {'type': 'string', 'required': True, 'minlength': 1,'maxlength': 1000},
        
        'status': {                 # TODO: make it readonly
            'type': 'string',
            'allowed': [
                'REQUESTED',        # Request initiated by the developer
                'REVOKED',          # Request revoked by the developer
                'APPROVED',         # Request approved
                'REJECTED',         # Request rejected
            ],
            'default': 'REQUESTED'
        },
        'extend_by': {              # extension in hours (max = 30 days)
            'type': 'number',
            'max': 7200,
            'required': True
        },
        'provision_request': {
            'type': 'objectid',
            'data_relation': {
                'resource': 'provisionRequests',
                'embeddable': True,
            },
            'required': True
        },
        'reviewed_by': {
            'type': 'objectid',
            'data_relation': {
                'resource': 'users',
                'embeddable': True,
            }
        },
        'requested_by': {             # Request created by
            'type': 'objectid',
            'data_relation': {
                'resource': 'users',
                'embeddable': True,
            },
            'required': True
        }
    }
}
