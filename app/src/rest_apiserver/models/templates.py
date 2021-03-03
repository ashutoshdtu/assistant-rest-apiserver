"""
    rest_apiserver.models.templates
    ~~~~~~~~~~~~~~~~~

    Schema for resource templates APIs. 

    :license: GPL-3.0, see LICENSE for more details.
"""

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
        # URL for template file (cluster.yaml for eksctl)
        'url': {'type': 'string', 'required': True},
        'type': {
            'type': 'string', 
            'required': True, 
            'default': 'EKSCTL', 
            'allowed': ['EKSCTL']
        },
        'params': {
            'type': 'list',
            'schema': {
                'type': 'string',
                'regex': '[a-zA-Z1-9_]+'        # check if proper variable name
            }
        }
    }
}
