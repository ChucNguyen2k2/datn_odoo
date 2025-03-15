{
    'name': 'School Attendance Log',
    'version': '1.0.0',
    'summary': 'Custom attendance tracking with geolocation and IP logging for school employees',
    'description': """
        Phân hệ chấm công dành cho nhân viên trong trường học bao gồm
        - Check in
        - Check out
        - Geolocation
        - IP logging
        """,
    'category': 'Human Resources',
    'author': 'ChucDEV',
    'depends': ['hr_attendance', 'base_geolocalize'],
    'data': [
        'security/access_rules.xml',
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
