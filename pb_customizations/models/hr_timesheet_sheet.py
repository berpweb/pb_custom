from openerp import models, api, fields

class HrTimesheetSheet(models.Model):
    _inherit = "hr_timesheet_sheet.sheet"
     
    attendanceslip_run_id = fields.Many2one('generate.timesheet', 'Attendance Slip Batches', readonly=True, copy=False)
    attendance_total_hours = fields.Char(string="Total Hours", compute='_get_total_hours', 
                                     default='0:0', copy=False)
    active = fields.Boolean(string="Active", default=True)
     
    @api.one
    @api.depends('attendances_ids')
    def _get_total_hours(self):
        attendance_hours, attendance_mins = 0,0
        attendance_times = self.attendances_ids.filtered(lambda attendance: attendance.action =='sign_out')
        total_attendance_times = attendance_times.mapped('view_hours')
        for attendance in total_attendance_times:
            if attendance and attendance != '0:0' and not '.' in attendance:
                hours_mins = attendance.split(':')
                attendance_hours += int(hours_mins[0]) if hours_mins else 0
                attendance_mins += int(hours_mins[1]) if hours_mins else 0
        attendance_seconds = (attendance_hours * 60 * 60) + (attendance_mins * 60)
        if attendance_seconds:
            attendance_hours = attendance_seconds/(60 * 60)
            attendance_mins = (attendance_seconds/(60)) % 60
        self.attendance_total_hours = '%s:%s'%(attendance_hours, attendance_mins)
    
    @api.multi
    def name_get(self):
        res = []
        for record in self:
            res.append((record.id, record.employee_id.name))
        return res
    
    @api.model
    def fields_get(self, *args, **kwargs):
        fields_to_show = ['employee_id', 'date_from', 'date_to']
        res = super(HrTimesheetSheet, self.sudo()).fields_get(*args, **kwargs)
        for k in res.iterkeys():
                if k not in fields_to_show:
                    res[k]['selectable'] = False
        return res