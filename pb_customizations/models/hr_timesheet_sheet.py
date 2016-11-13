from openerp import models, api, fields

class HrTimesheetSheet(models.Model):
    _inherit = "hr_timesheet_sheet.sheet"
     
    attendanceslip_run_id = fields.Many2one('generate.timesheet', 'Attendance Slip Batches', readonly=True, copy=False)
    
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