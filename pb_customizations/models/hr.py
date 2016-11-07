from openerp import models, api, fields

class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    
    user_id_rel = fields.Char(compute='compute_user_id', store=True)
    
    @api.depends('user_id')
    def compute_user_id(self):
        self.user_id_rel = self.user_id.id


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'
    
    emp_id_rel = fields.Char(compute='compute_emp_id', store=True)
    
    @api.depends('employee_id')
    def compute_emp_id(self):
        self.emp_id_rel = self.employee_id.id