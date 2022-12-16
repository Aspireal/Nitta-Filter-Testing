# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Nitta CRM Sequence',
    'version': '16.0',
    'category': 'Sales/CRM',
    'sequence': 1,
    'summary': 'Track leads and close opportunities',
    'description': "",
    'website': 'https://www.odoo.com/app/crm',
    'depends': ['base','web', 'crm'
    ],
    'data': [
       'views/crm_seq_views.xml'
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}