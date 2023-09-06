{
    'name': 'Google Sheets Sync',
    'version': '13.0.1.0.0',
    'summary': 'Google Sheets Sync Odoo',
    'description': 'Conecta Google Sheets con Odoo 13, al actualizar datos en Google Sheets actualiza los datos en Odoo',
    'license': 'AGPL-3',
    'sequence': -1,
    'depends': ['base'],
    'data': [
        'views/google_sheets_view.xml',
        'views/menus.xml',
        'security/ir.model.access.csv'
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
