import openerp
from openerp import models, api, fields

from openerp import tools

class Task(models.Model):
    _inherit = 'project.task'
    
    partner_id = fields.Many2one('res.partner', domain=[('customer', '=', 1)])
    user_id = fields.Many2one('res.users', default=False)
    customer_name = fields.Char(related='partner_id.name')
    customer_phone = fields.Char(related='partner_id.mobile')
    customer_address1 = fields.Char(related='partner_id.street')
    customer_address2 = fields.Char(related='partner_id.city')
    customer_state = fields.Char(related='partner_id.state_id.name')
    customer_zip = fields.Char(related='partner_id.zip')
    customer_country = fields.Char(related='partner_id.country_id.name')
    project_id = fields.Many2one('project.project', string='Project', required=True, readonly=True, default=lambda self: self.env['project.project'].search([], limit=1))
    app_project_id = fields.Char(compute='_get_project_id', store=True)
    app_analytic_account_id = fields.Char(compute='_get_analytic_account_id', store=True)
    task_start_time = fields.Char(string="Task start Time", default='-', copy=False)
    task_stop_time = fields.Char(string="Task Stop Time", default='-', copy=False)
    task_work_duration = fields.Char(string="Task Work Duration", default='-', copy=False)
    vehicle_start_time = fields.Char(string="Vehicle start Time", default='-', copy=False)
    vehicle_stop_time = fields.Char(string="Vehicle Stop Time", default='-', copy=False)
    vehicle_work_duration = fields.Char(string="Vehicle Work Duration", default='-', copy=False)
    task_done = fields.Char(string="Task Done", default='notok')
    vehicle_details = fields.Many2one('vehicle.vehicle', string="Vehicle Name", copy=False)
    vehicle_name = fields.Char(related='vehicle_details.name')
    vehicle_number = fields.Char(related='vehicle_details.vehicle_number')
    vehicle_name_number = fields.Char(string="Vehicle Name Number", default='-', copy=False)
    
    def _default_image(self):
        image_path = openerp.modules.get_module_resource('pb_customizations', 'static/src/img', 'default.png')
        return tools.image_resize_image_big(open(image_path, 'rb').read().encode('base64'))
    
    # images fields
    image = fields.Binary('Customer Signature', default=_default_image, attachment=True)
    image_medium = fields.Binary('Customer Signature', attachment=True)
    image_small = fields.Binary('Customer Signature', attachment=True)
    
    @api.multi
    def write(self, vals):
        if vals.get('task_done', False) and vals['task_done'] == "ok":
            vals['stage_id'] = self.env['project.task.type'].search([('is_closed', '=', True)], limit=1).id
            vals['timesheet_ids'] = [(0,0,{'date': self.vehicle_start_time.split()[0],
                                           'name': 'Vehicle Duration', 
                                           'task_start_time': self.vehicle_start_time,
                                           'task_stop_time': self.vehicle_stop_time,
                                           'task_work_duration': self.vehicle_work_duration,
                                           'user_id': self.user_id.id,
                                           'account_id': self.analytic_account_id.id}),
                                     (0,0,{'date': self.task_start_time.split()[0],
                                           'name': 'Work Duration', 
                                           'task_start_time': self.task_start_time,
                                           'task_stop_time': self.task_stop_time,
                                           'task_work_duration': self.task_work_duration,
                                           'user_id': self.user_id.id,
                                           'account_id': self.analytic_account_id.id})]
        if vals.get('vehicle_name_number', False):
            vehicle = vals['vehicle_name_number'].split(' - ')[0]
            vals['vehicle_details'] = self.env['vehicle.vehicle'].search([('name', '=', vehicle)], limit=1).id
        if vals.get('user_id', False):
            vals['user_id'] = int(vals['user_id'])
        return super(Task, self).write(vals)

    @api.model
    def fields_get(self, *args, **kwargs):
        fields_to_show = ['name', 'vehicle_details', 'stage_id']
        res = super(Task, self.sudo()).fields_get(*args, **kwargs)
        for k in res.iterkeys():
                if k not in fields_to_show:
                    res[k]['selectable'] = False
        return res
    
    @api.one
    @api.depends('project_id')
    def _get_project_id(self):
        self.app_project_id = self.project_id.id

    @api.one
    @api.depends('analytic_account_id')
    def _get_analytic_account_id(self):
        self.app_analytic_account_id = self.analytic_account_id.id
        

class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'
    
    is_closed = fields.Boolean(string="Is a closed stage?")