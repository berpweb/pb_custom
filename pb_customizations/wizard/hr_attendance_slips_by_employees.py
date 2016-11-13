from openerp import models, api, fields
from openerp.tools.translate import _
from openerp.exceptions import UserError

class HrAttendanceSlipsEmployees(models.TransientModel):

    _name ='hr.attendance.slips.employees'
    _description = 'Generate attendance slips for all selected employees'
    
    employee_ids = fields.Many2many('hr.employee', 'hr_employee_group_rel', 'att_slip_id', 'employee_id', 'Employees')
    
    @api.multi
    def compute_sheet(self):
        slip_pool = self.env['hr_timesheet_sheet.sheet']
        run_pool = self.env['generate.timesheet']
        for run in self:
            active_window = run_pool.browse(self.env.context.get('active_id'))
            from_date = active_window.date_start
            to_date = active_window.date_end
            if not run.employee_ids:
                raise UserError(_("You must select employee(s) to generate attendance payslip(s)."))
            for emp in run.employee_ids:
                res = {
                    'employee_id': emp.id,
                    'date_from': from_date,
                    'date_to': to_date,
                    'attendanceslip_run_id': active_window.id,
                }
                try:
                    slip_pool.create(res)
                except UserError, e:
                    raise e
                active_window.close_generate_timesheet_run()
        return {'type': 'ir.actions.act_window_close'}
