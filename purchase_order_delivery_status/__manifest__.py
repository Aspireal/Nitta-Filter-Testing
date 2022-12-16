# -*- coding: utf-8 -*-


{
    'name': "Delivery Status on Purchase Order",
    'summary': """Delivery Status on Purchase Order""",
    'description': "This module adds delivery status on purchase order",
    'author': "Cybrosys Techno Solutions",
    'company': "Cybrosys Techno Solutions",
    'website': "http://www.cybrosys.com",
    'category': 'Purchase',
    'version': '16.0.0.2',
    'depends': ['purchase', 'stock', 'purchase_stock'],
    'data': ['views/purchase_order.xml'],
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
}
