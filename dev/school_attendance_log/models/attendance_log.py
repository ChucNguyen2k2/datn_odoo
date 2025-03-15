from odoo import models, fields, api
from odoo.http import request
import geocoder
import socket

class AttendanceLog(models.Model):
    _name = 'school.attendance.log'
    _description = 'School Attendance Log with Geolocation and IP'
    _order = 'check_in desc'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    check_in = fields.Datetime(string='Check In', default=fields.Datetime.now)
    check_out = fields.Datetime(string='Check Out')
    location = fields.Char(string='Location', help='Geographical location based on IP')
    ip_address = fields.Char(string='IP Address', help='IP address of the device')
    latitude = fields.Float(string='Latitude')
    longitude = fields.Float(string='Longitude')

    @api.model
    def create(self, vals):
        ip_address = self._get_client_ip()
        vals['ip_address'] = ip_address

        if ip_address and ip_address != 'Unknown':
            latitude, longitude, location = self._get_geolocation(ip_address)
            vals['latitude'] = latitude
            vals['longitude'] = longitude
            vals['location'] = location

        return super(AttendanceLog, self).create(vals)

    def _get_client_ip(self):
        try:
            ip = request.httprequest.remote_addr if request else False
            return ip or 'Unknown'
        except Exception:
            return 'Unknown'

    def _get_geolocation(self, ip_address):
        try:
            g = geocoder.ip(ip_address)
            if g.ok:
                return g.latlng[0], g.latlng[1], g.address
            return 0.0, 0.0, 'Unknown'
        except Exception:
            return 0.0, 0.0, 'Geolocation unavailable'

    def attendance_manual(self):
        self.ensure_one()
        employee = self
        ip_address = self._get_client_ip()
        latitude, longitude, location = self._get_geolocation(ip_address)

        attendance = self.env['school.attendance.log'].search([
            ('employee_id', '=', employee.id),
            ('check_out', '=', False)
        ], limit=1)

        if attendance:
            attendance.write({
                'check_out': fields.Datetime.now(),
                'latitude': latitude,
                'longitude': longitude,
                'location': location,
            })
        else:
            self.env['school.attendance.log'].create({
                'employee_id': employee.id,
                'check_in': fields.Datetime.now(),
                'latitude': latitude,
                'longitude': longitude,
                'location': location,
                'ip_address': ip_address,
            })

        employee._attendance_action_change()
        return {'type': 'ir.actions.act_window_close'}