from odoo import models, fields, api
from odoo.exceptions import ValidationError
import geopy.geocoders
from geopy.exc import GeocoderTimedOut
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
        # Lấy địa chỉ IP của thiết bị
        ip_address = self._get_client_ip()
        vals['ip_address'] = ip_address

        # Lấy geolocation dựa trên IP
        if ip_address:
            latitude, longitude, location = self._get_geolocation(ip_address)
            vals['latitude'] = latitude
            vals['longitude'] = longitude
            vals['location'] = location

        return super(AttendanceLog, self).create(vals)

    def _get_client_ip(self):
        """Lấy địa chỉ IP của máy client."""
        try:
            ip = self.env['ir.http']._get_client_ip()
            return ip or 'Unknown'
        except Exception:
            return 'Unknown'

    def _get_geolocation(self, ip_address):
        """Lấy thông tin địa điểm dựa trên IP sử dụng geopy."""
        try:
            geolocator = geopy.geocoders.Nominatim(user_agent="school_attendance_log")
            location = geolocator.geocode(ip_address, language='en')
            if location:
                return location.latitude, location.longitude, location.address
            return 0.0, 0.0, 'Unknown'
        except (GeocoderTimedOut, ValueError):
            return 0.0, 0.0, 'Geolocation unavailable'

    def attendance_manual(self, employee_id, latitude, longitude):
        employee = self.env['hr.employee'].browse(employee_id)
        if not employee:
            return {'success': False, 'message': 'Employee not found'}

        # Kiểm tra trạng thái chấm công hiện tại
        attendance = self.search([('employee_id', '=', employee.id), ('check_out', '=', False)], limit=1)
        if attendance:
            attendance.write({
                'check_out': fields.Datetime.now(),
                'latitude': latitude,
                'longitude': longitude,
            })
        else:
            self.create({
                'employee_id': employee.id,
                'check_in': fields.Datetime.now(),
                'latitude': latitude,
                'longitude': longitude,
            })
        return {'success': True}
