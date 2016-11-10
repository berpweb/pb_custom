# -*- coding: utf-8 -*-

from openerp import api, fields, models, _


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'
    
    
    task_start_time = fields.Datetime(string="Punch In Time")
    task_stop_time = fields.Datetime(string="Punch Out Time")