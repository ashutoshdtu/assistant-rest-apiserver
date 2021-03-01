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
