{
    'name': 'School HR Management',
    'version': '1.0.0',
    'summary': 'Quản lý nhân viên và phòng ban trong trường học',
    'sequence': -100,
    'description': """
        Phân hệ quản lý nhân sự trong trường học bao gồm:
        - Quản lý thông tin nhân viên.
        - Quản lý thông tin phòng ban.
    """,
    'category': 'Human Resources',
    'author': 'ChucDEV',
    'depends': ['base'],
    'data': [
        'security/models_access.xml',  # Quyền truy cập XML
        'security/ir.model.access.csv',  # Quyền truy cập CSV
        'views/employee_views.xml',
        'views/department_views.xml',
        'views/menu_views.xml',
        'data/sequence.xml',  # File sequence (thêm mới)
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}