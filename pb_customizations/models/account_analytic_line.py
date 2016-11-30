# -*- coding: utf-8 -*-

from openerp import api, fields, models
from openerp.exceptions import UserError
from datetime_utilities import valid_date, compute_hours_mins

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'
    
    task_start_time = fields.Char(string="Punch In Time")
    task_stop_time = fields.Char(string="Punch Out Time")
    task_work_duration = fields.Char(string="Work Duration")
    update_value = fields.Char(string="Update Value", copy=False)
    to_update = fields.Selection([('in', 'Punch In'),
                                  ('out', 'Punch Out')])
    
    @api.multi
    @api.onchange('update_value')
    def on_change_update_value(self):
        if self.update_value and not valid_date(self.update_value, '%m/%d/%Y %I:%M:%S %p'):
            self.update_value = False
            return {'warning': {
                        'title': 'Error!',
                        'message': 'Please enter the correct format!'}}
    
    @api.model
    def create(self, vals):
        if vals.get('task_id', False):
            vals['task_id'] = int(vals['task_id'])
        if vals.get('account_id', False):
            vals['account_id'] = int(vals['account_id'])
        return super(AccountAnalyticLine, self.sudo()).create(vals)
    
    @api.multi
    def update_data(self):
        if self.to_update == 'in':
            duration = compute_hours_mins(self.update_value, self.task_stop_time, '%m/%d/%Y %I:%M:%S %p')
            self.task_work_duration = duration
            self.task_start_time = self.update_value
        elif self.to_update == 'out':
            duration = compute_hours_mins(self.task_start_time, self.update_value, '%m/%d/%Y %I:%M:%S %p')
            self.task_work_duration = duration
            self.task_stop_time = self.update_value
        else:
            self.update_value = False
            raise UserError('Please select punch in/out to update!')
        