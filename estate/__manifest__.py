{
    'name': "Real Estate",
    'version': '1.0',
    'description': 'A module for managing real estate properties.',
    'depends': ['base'],
    'author': "Herie",
    'category': 'Category',
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/RE.png'],
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_menus.xml',
        'views/estate_property_offer_view.xml',
        'views/estate_property_type_view.xml',
        'views/estate_property_tag_view.xml',
        'data/property_type_data.xml'
    ]
}