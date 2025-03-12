from odoo import models, fields, api, exceptions as ValidationError

class Employee(models.Model):
    _name = 'school.employee'
    _description = 'Employee Management'

    name = fields.Char(string='Họ và tên', required=True)
    code = fields.Char(string='Mã nhân viên', required=True, copy=False, readonly=True, default=lambda self: 'New')
    position = fields.Selection([
        ('manager', 'Trưởng phòng'),
        ('vice_manager', 'Phó phòng'),
        ('staff', 'Nhân viên'),
    ], string='Chức vụ', required=True)
    manager_id = fields.Many2one('school.employee', string='Người quản lý', readonly=True)
    department_id = fields.Many2one('school.department', string='Phòng ban')
    contract_code = fields.Char(string='Mã hợp đồng lao động')
    address = fields.Char(string='Địa chỉ')
    phone = fields.Char(string='Số điện thoại')
    date_of_birth = fields.Date(string='Ngày sinh')
    gmail = fields.Char(string='Email', help='Địa chỉ email của nhân viên')
    image = fields.Binary(string='Ảnh nhân viên', attachment=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('code', 'New') == 'New':
                vals['code'] = self.env['ir.sequence'].next_by_code('school.employee') or 'New'
        return super(Employee, self).create(vals_list)

    @api.onchange('department_id')
    def _onchange_department(self):
        if self.department_id and self.position != 'manager':
            self.manager_id = self.department_id.manager_id.id if self.department_id.manager_id else False

    @api.constrains('phone')
    def _check_phone_number(self):
        for rec in self:
            if rec.phone and (len(rec.phone) != 10 or not rec.phone.isdigit() or not rec.phone.startswith('0')):
                raise ValidationError("Số điện thoại phải là 10 ký tự, chỉ gồm số và bắt đầu bằng số 0.")

    def action_save(self):
        """Lưu thông tin nhân viên"""
        return True

    def action_delete(self):
        """Xóa nhân viên hiện tại với xác nhận và kiểm tra"""
        for rec in self:
            # Kiểm tra nếu nhân viên là trưởng phòng của phòng ban nào đó
            if rec.position == 'manager' and rec.department_id.manager_id == rec:
                raise ValidationError("Không thể xóa nhân viên này vì họ là trưởng phòng của phòng ban '%s'!" % rec.department_id.name)
            # Hiển thị thông báo xác nhận (đã được xử lý bởi thuộc tính confirm trong XML)
            rec.unlink()