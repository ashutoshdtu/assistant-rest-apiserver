notifications = {
    'item_title': 'notification',
    
    'resource_methods': ["POST", "GET"],
    'item_methods': ["GET", "DELETE"],

    'datasource': {
        'source': 'notifications', 
        'default_sort': [('_created', -1)]
    },

    'schema': {
        'title': {'type': 'string', 'required': True, 'maxlength': 200},
        'description': {'type': 'string', 'maxlength': 500},
        'user': {
            'type': 'objectid',
            'data_relation': {
                'resource': 'users',
                'embeddable': True,
            },
            'required': True
        },
        'channels': {
            'type': 'list',
            'schema': {
                'type': 'string',
                'default': 'EMAIL',
                'allowed': ['EMAIL']    #['EMAIL', 'SLACK', 'SMS']
            },
        },
        'status': {
            'type': 'string', 
            'default': 'CREATED', 
            'allowed': ['SENT','CREATED'],
        }
    }
}
