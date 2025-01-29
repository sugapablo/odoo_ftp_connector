{
    'name': 'Odoo FTP Connector',
    'version': '0.2',
    'summary': 'Connects Odoo with FTP server',
    'description': 'This module allows Odoo to connect with an FTP server and perform file operations.',
    'category': 'Tools',
    'author': 'Russ Schneider',
    'website': 'https://www.redlabmedia.com',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/ftp.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
