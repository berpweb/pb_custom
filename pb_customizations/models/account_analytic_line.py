# -*- coding: utf-8 -*-

from openerp import api, fields, models

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'
    
    
    task_start_time = fields.Char(string="Punch In Time")
    task_stop_time = fields.Char(string="Punch Out Time")
    task_work_duration = fields.Char(string="Work Duration")
    
#     @api.onchange('task_work_duration')
#     def on_change_task_work_duration(self):
#         try:
#             self.task_work_duration.split(':')[1] if self.task_work_duration else 0
#         except IndexError:
#             self.task_work_duration = "%s:%s"%(self.task_work_duration.split(':')[0], 0)
#         else:
#             pass
    
    @api.model
    def create(self, vals):
        if vals.get('task_id', False):
            vals['task_id'] = int(vals['task_id'])
        if vals.get('account_id', False):
            vals['account_id'] = int(vals['account_id'])
        return super(AccountAnalyticLine, self.sudo()).create(vals)
    