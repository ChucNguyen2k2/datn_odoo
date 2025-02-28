from odoo import models, fields


class HrDepartment(models.Model):
    _inherit = 'hr.department'

    facility = fields.Selection([
        ('north', 'Phía Bắc'),
        ('south', 'Phía Nam')
    ], string='Cơ sở', required=True, default='north')


    department_type = fields.Selection([
    ('director', 'Ban Giám đốc'),
    ('functional', 'Cơ quan chức năng'),
    ('faculty', 'Khoa giảng viên'),
    ('management', 'Hệ quản lý')
], string='Loại phòng ban', required=True)
