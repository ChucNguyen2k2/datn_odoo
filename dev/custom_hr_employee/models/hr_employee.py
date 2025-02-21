from odoo import models, fields

class EmployeeCustom(models.Model):
    _inherit = 'hr.employee'  # Kế thừa từ module nhân viên của Odoo

    subject_teach = fields.Char(string="Môn Giảng Dạy")
    homeroom_class = fields.Char(string="Lớp Chủ Nhiệm")
    education_level = fields.Selection([
        ('bachelor', 'Cử nhân'),
        ('master', 'Thạc sĩ'),
        ('phd', 'Tiến sĩ'),
    ], string="Trình độ chuyên môn")
    work_schedule = fields.Text(string="Thời gian làm việc")
