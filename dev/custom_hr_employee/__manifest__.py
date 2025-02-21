{
    'name': 'Custom HR Employee for School',
    'version': '1.0',
    'summary': 'Tùy chỉnh module nhân viên cho trường học',
    'author': 'Your Name',
    'category': 'Human Resources',
    'depends': ['hr', 'website'],
    'data': [
        'views/hr_employee_views.xml',
        'views/custom_employee_template.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'custom_hr_employee/static/src/scss/custom_style.scss',
        ],
    },
    'installable': True,
    'application': False,
}
