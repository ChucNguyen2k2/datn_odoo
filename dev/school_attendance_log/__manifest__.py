{
    'name': 'School Attendance Log',
    'version': '1.0.0',
    'summary': 'Custom attendance tracking with geolocation and IP logging for school employees',
    'description': """
        This module enhances the Odoo attendance system with custom design, geolocation, and IP logging for school employees.
    """,
    'category': 'Human Resources',
    'author': 'ChucDEV',
    'depends': ['hr_attendance', 'base_geolocalize'],
    'data': [
        'security/ir.model.access.csv',
        'views/attendance_log_views.xml',
        'views/assets.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
    'external_dependencies': {
        'python': ['geopy'],
    },
}
