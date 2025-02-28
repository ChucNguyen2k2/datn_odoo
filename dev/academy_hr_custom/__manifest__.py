{
    'name': "Academy HR Custom",
    'summary': "Custom HR module for Academy of Cryptography Techniques",
    'description': "...",
    'author': "Your Name",
    'version': '1.0',
    'depends': ['hr', 'website'],  # Thêm 'website' nếu dùng template
    'data': [
        'views/hr_employee_views.xml',
        'views/hr_department_views.xml',
        'views/templates.xml',
        'data/hr_data.xml',
    ],
    'installable': True,
    'application': False,
}