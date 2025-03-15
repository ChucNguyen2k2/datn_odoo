{
    'name': 'My Library',
    'version': '1.0.0',
    'author': 'ChucDev',
    'summary': 'Quản lý sách trong thư viện',
    'description': 'Module đơn giản để quản lý sách',
    'category': 'Tools',
    'depends': ['base', 'mail'],
    'data': [
        'security/access_rules.xml',
        'views/attendance_log_views.xml',
        'views/assets.xml',
    ],
    'asset': {
        'web.assets_backend': [
            'my_library/static/src/css/library_book.css'
        ]
    },
    'images': ['static/description/icon.png'],
    'installable': True,
    'auto_install': False,
    'application': True,
}
