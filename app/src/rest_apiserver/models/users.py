"""
    rest_apiserver.models.users
    ~~~~~~~~~~~~~~~~~

    Schema for Users, Roles, Quotas and Estimated Bills APIs.

    :license: GPL-3.0, see LICENSE for more details.
"""

users = {
    'item_title': 'user',
    
    'resource_methods': ["POST", "GET"],
    'item_methods': ["GET", "PUT", "PATCH", "DELETE"],

    'datasource': {
        'source': 'users', 
        # 'projection': {'password': 0},
        'default_sort': [('_created', -1)]
    },

    'extra_response_fields': ["email", "roles"],

    'schema': {
        # '_id': {'type': 'objectid', 'unique': True, 'required': True}, # custom id type
        'name': {'type': 'string', 'minlength': 1, 'maxlength': 100},
        'email': {'type': 'string'},
        'username': {'type': 'string', 'required': True, 'unique': True, 'minlength': 1,'maxlength': 100},
        # 'password': {'type': 'string', 'required': False},
        'roles': {
            'type': 'list',
            'schema': {
                'type': 'string',
                'data_relation': {
                    'resource': 'roles',
                    'embeddable': True,
                    'field': 'role',
                },
            },
            'required': False
        },
        'isActive': { 'type': 'boolean', 'default': True },
        'status': {
            'type': 'string', 
            'default': 'CREATED', 
            'allowed': ['INVITED','CREATED','VERIFIED'],
        }
    }
}

roles = {
    'item_title': 'role',

    'item_url': 'regex("[a-zA-Z0-9-_]+")',
    
    'resource_methods': ["POST", "GET"],
    'item_methods': ["GET", "PUT", "DELETE"],

    'datasource': {
        'source': 'roles', 
        'default_sort': [('_created', -1)]
    },

    'schema': {
        'role': {'type': 'string', 'required': True, 'unique': True, 'minlength': 1,'maxlength': 100},
        'description': {'type': 'string', 'maxlength': 200},
        'isActive': { 'type': 'boolean', 'default': True },
    },
}

# API schemas for quotas
quotas = {
    'item_title': 'quota',

    'resource_methods': ["POST", "GET"],
    'item_methods': ["GET", "PUT", "PATCH", "DELETE"],

    'datasource': {
        'source': 'quotas', 
        'default_sort': [('_created', -1)]
    },

    'schema': {
        # 'quota_type': {'type': 'string', 'required': True, 'minlength': 1,'maxlength': 100},
        'quota_type': {
            'type': 'string',
            'default': 'TEMPORARY',
            'allowed': ['TEMPORARY', 'PERMANENT']
        },
        'user': {
            'type': 'objectid',
            'data_relation': {
                'resource': 'users',
                'embeddable': True,
            },
            'required': False
        },
        'role': {
            'type': 'string',
            'data_relation': {
                'resource': 'roles',
                'embeddable': True,
                'field': 'role',
            },
            'required': False
        },
        # cost per in USD
        'cost': { 'type': 'number', 'default': 100, 'max': 10000},
        'machines': {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    'instance_type': { 'type': 'string', 'minlength': 1, 'maxlength': 30, 'required': True },
                    'region': { 'type': 'string', 'required': True },
                    'hours': { 'type': 'number', 'required': True, 'max': 50000 }
                },
            },
        },
        'disk': {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    'disk_type': { 'type': 'string', 'minlength': 1, 'maxlength': 30, 'required': True },
                    'region': { 'type': 'string', 'required': True },
                    'gbhours': { 'type': 'number', 'required': True, 'max': 1000000 } # gb * hours
                },
            },
        },
        's3': {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    'bucket_type': { 'type': 'string', 'minlength': 1, 'maxlength': 30, 'required': True },
                    'region': { 'type': 'string', 'required': True },
                    'gbhours': { 'type': 'number', 'required': True, 'max': 1000000 } # gb * hours
                },
            },
        }
    }
}

estimatedBills = {
    'item_title': 'estimatedBill',

    'item_url': 'regex("[a-zA-Z0-9-_]+")',
    
    'resource_methods': ["POST", "GET"],
    'item_methods': ["GET", "PUT", "DELETE"],

    'datasource': {
        'source': 'estimatedBills', 
        'default_sort': [('_created', -1)]
    },

    'schema': {
        'estimated_bill': {'type': 'string', 'required': True, 'unique': True, 'minlength': 1,'maxlength': 100},
        'user': {
            'type': 'objectid',
            'data_relation': {
                'resource': 'users',
                'embeddable': True,
            },
            'required': True
        },
        'month': { 'type': 'number', 'required': True, 'min': 1, 'max': 12 },
        'year': {'type': 'number', 'required': True, 'min': 2000, 'max': 2100}
    },
}