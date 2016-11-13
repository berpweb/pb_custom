from openerp import models, api, fields
from openerp.exceptions import ValidationError
from datetime import datetime

class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    
    user_id_rel = fields.Char(compute='compute_user_id', store=True)
    
    @api.one
    @api.depends('user_id')
    def compute_user_id(self):
        self.user_id_rel = self.user_id.id
            
    @api.one
    @api.constrains('user_id')
    def _check_user_for_emp(self):
        if self.user_id and self.search([('user_id', '=', self.user_id.id), ('id', '!=', self.id)]).ids:
            raise ValidationError('You cannot assign same user to multiple employees.')
        
    @api.model
    def fields_get(self, *args, **kwargs):
        fields_to_show = ['name', 'mobile_phone', 'work_email']
        res = super(HrEmployee, self.sudo()).fields_get(*args, **kwargs)
        for k in res.iterkeys():
                if k not in fields_to_show:
                    res[k]['selectable'] = False
        return res


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'
    
    emp_id_rel = fields.Char(compute='compute_emp_id', store=True)
    punch_out_address = fields.Char(string="Punch Out Location")
    view_date = fields.Char(compute='_get_attendace_date', store=True, string="Date")
    view_out_time = fields.Char(compute='_get_attendace_date', store=True, string="Punch Out Time")
    
    @api.one
    @api.depends('employee_id')
    def compute_emp_id(self):
        self.emp_id_rel = self.employee_id.id
            
    @api.model
    def create(self, vals):
        if vals.get('employee_id', False):
            vals['employee_id'] = int(vals['employee_id'])
        return super(HrAttendance, self.sudo()).create(vals)
    
    @api.one
    @api.depends('name')
    def _get_attendace_date(self):
        d = datetime.strptime(self.name, '%Y-%m-%d %H:%M:%S')
        day_string = d.strftime('%d/%m/%Y')
        time_string = d.strftime('%H:%M:%S')
        self.view_date = day_string
        self.view_out_time = time_string
    