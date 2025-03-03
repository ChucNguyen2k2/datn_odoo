{
    'name': 'My Library',
    'version': '1.0.0',
    'author': 'ChucDev',
    'summary': 'Quản lý sách trong thư viện',
    'description': 'Module đơn giản để quản lý sách',
    'category': 'Tools',
    'depends': ['base', 'mail'],
    'data': [
        'views/library_book_views.xml',
        'security/ir.model.access.csv',
    ],
    'asset': {
        'web.assets_backend': [
            'my_library/static/src/css/library_book.css'
        ]
    },
    'installable': True,
    'auto_install': False,
    'application': True,
}