from odoo import http
from odoo.http import request

class CustomEmployeeController(http.Controller):
    @http.route('/employees', type='http', auth='public', website=True)
    def custom_employee_page(self):
        employees = request.env['hr.employee'].sudo().search([])
        return request.render('custom_hr_employee.custom_employee_template', {'employees': employees})
