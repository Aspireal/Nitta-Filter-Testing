# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Nitta Purchase Customization ',
    'version': '16.0.0.2',
    'category': 'Purchase',
    'sequence': 1,
    'summary': 'it is used Track the Record',
    'description': "",
    'website': 'https://www.odoo.com/app/crm',
    'depends': ['base', 'purchase', 'purchase_isolated_rfq'
                ],
    'data': [
        'views/purchase_views.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
