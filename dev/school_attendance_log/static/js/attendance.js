odoo.define('school_attendance_log.attendance', function (require) {
    "use strict";

    var core = require('web.core');
    var publicWidget = require('web.public.widget');
    var _t = core._t;

    publicWidget.registry.AttendanceWidget = publicWidget.Widget.extend({
        selector: '.btn-attendance',
        events: {
            'click': '_onAttendanceClick',
        },

        _onAttendanceClick: function (ev) {
            var self = this;
            var employeeId = $(ev.currentTarget).data('employeeId');

            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function (position) {
                    var latitude = position.coords.latitude;
                    var longitude = position.coords.longitude;
                    self._performAttendance(employeeId, latitude, longitude);
                }, function (error) {
                    self._performAttendance(employeeId, 0.0, 0.0);
                });
            } else {
                self._performAttendance(employeeId, 0.0, 0.0);
            }
        },

        _performAttendance: function (employeeId, latitude, longitude) {
            var self = this;
            this._rpc({
                model: 'hr.employee',
                method: 'attendance_manual',
                args: [employeeId, latitude, longitude],
            }).then(function (result) {
                if (result.success) {
                    self.displayNotification({
                        title: _t("Success"),
                        message: _t("Attendance recorded successfully!"),
                        type: 'success',
                    });
                    location.reload();
                } else {
                    self.displayNotification({
                        title: _t("Error"),
                        message: _t("Failed to record attendance."),
                        type: 'danger',
                    });
                }
            });
        },
    });
});