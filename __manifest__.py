{
    'name': 'Goddess Story Management',
    'version': '0.1',
    'depends': [
        'base',
        'product',
        'stock',
        'mrp',
        'point_of_sale',
        'uom',
        'website_sale'
    ],
    'data': [
        'security/ir.model.access.csv',

        'views.xml',
        'ecommerce_categories.xml',
        'data.xml'
    ],
    'installable': True,
    'application': True,
}