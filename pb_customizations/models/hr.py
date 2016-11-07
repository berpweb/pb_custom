from openerp import models, api, fields

class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    
    user_id_rel = fields.Char(compute='compute_user_id', store=True)
    
    @api.depends('user_id')
    def compute_user_id(self):
        for emp in self:
            emp.user_id_rel = emp.user_id.id


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'
    
    emp_id_rel = fields.Char(compute='compute_emp_id', store=True)
    
    @api.depends('employee_id')
    def compute_emp_id(self):
        for emp in self:
            emp.emp_id_rel = emp.employee_id.id