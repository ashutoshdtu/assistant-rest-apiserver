"""
    rest_apiserver.models.aws_pricing
    ~~~~~~~~~~~~~~~~~

    Schema for various AWS Resource Pricing APIs. 

    :license: GPL-3.0, see LICENSE for more details.
"""

""" AWS resource pricing APIs"""
# TODO: integrate with AWS Price list service API and depricate below APIs
# https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/using-pelong.html
instancePricing = {
    'resource_methods': ["POST", "GET"],
    'item_methods': ["GET", "PUT", "PATCH", "DELETE"],

    'datasource': {
        'source': 'instancePricing', 
        'default_sort': [('_created', -1)]
    },

    'schema': {
        'instance_type': {'type': 'string', 'required': True, 'maxlength': 100},
        'region': {'type': 'string', 'required': True, 'minlength': 1, 'maxlength': 40},
        'pricing_model': {
            'type': 'string', 
            'default': 'ON-DEMAND',
            'allowed': ['ON_DEMAND', 'SPOT', 'RESERVED', 'DEDICATED', '1YR-PARTIAL-PAY', '1YR-COMMITMENT', '3YR-COMMITMENT'],
            'required': True
        },
        'os': {
            'type': 'string', 
            'default': 'LINUX',
            'allowed': ['LINUX', 'WINDOWS'],
            'required': True
        },
        'cost_per_hour_usd': {      # in USD
            'type': 'float',
            'min': 0,
            'required': True
        }
    }
}

diskPricing = {
    'resource_methods': ["POST", "GET"],
    'item_methods': ["GET", "PUT", "PATCH", "DELETE"],

    'datasource': {
        'source': 'diskPricing', 
        'default_sort': [('_created', -1)]
    },

    'schema': {
        'disk_type': {'type': 'string', 'required': True, 'maxlength': 100},
        'region': {'type': 'string', 'required': True, 'minlength': 1, 'maxlength': 40},
        'pricing_model': {
            'type': 'string', 
            'default': 'ON-DEMAND',
            'allowed': ['ON_DEMAND', 'SPOT', 'RESERVED', 'DEDICATED', '1YR-PARTIAL-PAY', '1YR-COMMITMENT', '3YR-COMMITMENT'],
            'required': True
        },
        'cost_per_hour_usd': {      # in USD
            'type': 'float',
            'min': 0,
            'required': True
        }
    }
}
