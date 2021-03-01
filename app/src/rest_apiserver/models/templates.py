
templates = {
    'item_title': 'template',
    'item_url': 'regex("[a-zA-Z0-9-_]+")',

    'resource_methods': ["POST", "GET"],
    'item_methods': ["GET", "PUT", "DELETE"],

    'datasource': {
        'default_sort': [('_created', -1)]
    },

    'schema': {
        '_id': {'type': 'string', 'regex': '[a-z1-9-]+'}, #, 'unique': True}, # custom id type
        'name': {'type': 'string', 'required': True},
        'clusteryaml': {'type': 'string'},
        'params': {
            'type': 'list',
            'schema': {
                'type': 'string',
                'regex': '[a-zA-Z1-9_]+'        # check if proper variable name
            }
        }
    }
}
