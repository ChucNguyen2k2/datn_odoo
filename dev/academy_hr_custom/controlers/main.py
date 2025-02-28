from odoo import http
from odoo.http import request

class AcademyHRController(http.Controller):
    @http.route('/academy/employees', type='http', auth='public', website=True)
    def list_employees(self, **kwargs):
        # Lấy danh sách nhân viên từ model hr.employee
        employees = request.env['hr.employee'].sudo().search([])
        # Render template với dữ liệu nhân viên
        return request.render('academy_hr_custom.employee_list_template', {
            'employees': employees
        })

    @http.route('/academy/employee/<int:employee_id>', type='http', auth='public', website=True)
    def employee_detail(self, employee_id, **kwargs):
        # Lấy thông tin chi tiết của một nhân viên
        employee = request.env['hr.employee'].sudo().browse(employee_id)
        if not employee.exists():
            return request.render('website.404')
        return request.render('academy_hr_custom.employee_detail_template', {
            'employee': employee
        })