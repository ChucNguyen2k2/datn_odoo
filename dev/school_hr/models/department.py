from odoo import models, fields, api, exceptions as ValidationError

class Department(models.Model):
    _name = 'school.department'
    _description = 'Department Management'

    name = fields.Char(string='Tên phòng ban', required=True)
    manager_id = fields.Many2one('school.employee', string='Trưởng phòng', domain=[('position', '=', 'manager')])
    employee_ids = fields.One2many('school.employee', 'department_id', string='Danh sách nhân viên')

    _sql_constraints = [
        ('unique_manager_per_department', 'UNIQUE(manager_id)', 'Mỗi phòng ban chỉ được có một trưởng phòng!'),
    ]

    @api.constrains('manager_id')
    def _check_manager_position(self):
        for rec in self:
            if rec.manager_id and rec.manager_id.position != 'manager':
                raise ValidationError("Trưởng phòng phải có chức vụ là 'Trưởng phòng'.")

    def action_save(self):
        """Lưu thông tin phòng ban"""
        return True

    def action_delete(self):
        """Xóa phòng ban hiện tại với xác nhận và kiểm tra"""
        for rec in self:
            # Kiểm tra nếu phòng ban có nhân viên
            if rec.employee_ids:
                raise ValidationError("Không thể xóa phòng ban '%s' vì vẫn còn nhân viên thuộc phòng ban này!" % rec.name)
            # Hiển thị thông báo xác nhận (đã được xử lý bởi thuộc tính confirm trong XML)
            rec.unlink()