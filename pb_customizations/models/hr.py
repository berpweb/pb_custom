from openerp import models, api, fields
from openerp.exceptions import ValidationError

class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    
    user_id_rel = fields.Char(compute='compute_user_id', store=True)
    
    @api.depends('user_id')
    def compute_user_id(self):
        for emp in self:
            emp.user_id_rel = emp.user_id.id
            
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
    
    @api.depends('employee_id')
    def compute_emp_id(self):
        for emp in self:
            emp.emp_id_rel = emp.employee_id.id
            
    @api.model
    def create(self, vals):
        if vals.get('employee_id', False):
            vals['employee_id'] = int(vals['employee_id'])
        return super(HrAttendance, self.sudo()).create(vals)
    