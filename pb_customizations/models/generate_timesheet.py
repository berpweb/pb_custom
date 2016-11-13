from openerp import models, api, fields
from openerp.exceptions import ValidationError

class GenerateTimesheet(models.Model):
    _name = 'generate.timesheet'
    
    name = fields.Char(string='Name', required=True, readonly=True, states={'draft': [('readonly', False)]})
    state = fields.Selection([
            ('draft', 'Draft'),
            ('close', 'Close'),
        ], 'Status', index=True, readonly=True, copy=False, default='draft')
    date_start = fields.Date(string='Date From', required=True, readonly=True, states={'draft': [('readonly', False)]})
    date_end = fields.Date(string='Date To', required=True, readonly=True, states={'draft': [('readonly', False)]})
    slip_ids = fields.One2many('hr_timesheet_sheet.sheet', 'attendanceslip_run_id', 'Attendance Slips', required=False)
    
    @api.multi
    def close_generate_timesheet_run(self):
        return self.write({'state':'close'})
        
    @api.model
    def fields_get(self, *args, **kwargs):
        fields_to_show = ['name', 'date_start', 'date_end']
        res = super(GenerateTimesheet, self.sudo()).fields_get(*args, **kwargs)
        for k in res.iterkeys():
                if k not in fields_to_show:
                    res[k]['selectable'] = False
        return res