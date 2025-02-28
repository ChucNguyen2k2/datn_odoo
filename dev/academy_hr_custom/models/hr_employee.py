from odoo import models, api, fields
from odoo.exceptions import ValidationError


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    facility = fields.Selection([
        ('north', 'Phía Bắc'),
        ('south', 'Phía Nam')
    ], string='Cơ sở', required=True, default='north')

    deparment_type = fields.Selection([
        ('director', 'Ban Giám Đốc'),
        ('functional', 'Cơ quan chức năng'),
        ('faculty', 'Khoa giảng viên'),
        ('management', 'Hệ quản lý'),
    ], string='Loại phòng ban', required=True)

    position = fields.Selection([
        ('manager', 'Trưởng phòng'),
        ('deputy', 'Phó phòng'),
        ('staff', 'Nhân viên'),
        ('faculty_head', 'Trưởng khoa'),
        ('faculty_deputy', 'Phó khoa'),
        ('lecturer', 'Giảng viên')
    ], string='Chức vụ', required=True)

    # Validation cho các trường
    @api.constrains('facility', 'department_type', 'position', 'department_id')
    def _check_required_fields(self):
        for record in self:
            if not record.facility:
                raise ValidationError("Cơ sở không được để trống!")
            if not record.department_type:
                raise ValidationError("Loại phòng ban không được để trống!")
            if not record.position:
                raise ValidationError("Chức vụ không được để trống!")
            if not record.department_id:
                raise ValidationError("Phòng ban/Khoa không được để trống!")
            # Kiểm tra logic giữa department_type và position
            if record.department_type == 'faculty' and record.position not in ['faculty_head', 'faculty_deputy',
                                                                               'lecturer']:
                raise ValidationError("Chức vụ không phù hợp với Khoa giảng viên!")
            elif record.department_type != 'faculty' and record.position in ['faculty_head', 'faculty_deputy',
                                                                             'lecturer']:
                raise ValidationError("Chức vụ chỉ áp dụng cho Khoa giảng viên!")
            # Đảm bảo chỉ có 1 Trưởng khoa hoặc Trưởng phòng trong mỗi phòng ban
            if record.position in ['manager', 'faculty_head']:
                existing_head = self.env['hr.employee'].search([
                    ('department_id', '=', record.department_id.id),
                    ('position', 'in', ['manager', 'faculty_head']),
                    ('id', '!=', record.id)
                ])
                if existing_head:
                    raise ValidationError(
                        f"Đã có {existing_head.name} là Trưởng phòng/Trưởng khoa trong {record.department_id.name}!")

    # Giới hạn lựa chọn chức vụ dựa trên loại phòng ban
    @api.onchange('department_type')
    def _onchange_department_type(self):
        if self.department_type == 'faculty':
            return {'domain': {'position': [('position', 'in', ['faculty_head', 'faculty_deputy', 'lecturer'])]}}
        else:
            return {'domain': {'position': [('position', 'in', ['manager', 'deputy', 'staff'])]}}

    # Tự động gán người quản lý nếu là Trưởng phòng/Trưởng khoa
    @api.onchange('position', 'department_id')
    def _onchange_position(self):
        if self.position in ['manager', 'faculty_head'] and self.department_id:
            self.department_id.manager_id = self
