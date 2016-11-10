from openerp import models, api, fields

class Task(models.Model):
    _inherit = 'project.task'
    
    partner_id = fields.Many2one('res.partner', domain=[('customer', '=', 1)])
    customer_name = fields.Char(related='partner_id.name')
    customer_phone = fields.Char(related='partner_id.mobile')
    customer_address1 = fields.Char(related='partner_id.street')
    customer_address2 = fields.Char(related='partner_id.city')
    customer_zip = fields.Char(related='partner_id.zip')
    customer_country = fields.Many2one(related='partner_id.country_id')
    project_id = fields.Many2one('project.project', string='Project', required=True, readonly=True, default=lambda self: self.env['project.project'].search([], limit=1))
    task_start_time = fields.Datetime(string="Task start Time")
    task_stop_time = fields.Datetime(string="Task Stop Time")
    task_work_duration = fields.Float(string="Task Work Duration")
    vehicle_details = fields.Many2one('vehicle.vehicle', string="Vehicle Name")

    @api.model
    def fields_get(self, *args, **kwargs):
        fields_to_show = ['name', 'vehicle_details', 'stage_id']
        res = super(Task, self.sudo()).fields_get(*args, **kwargs)
        for k in res.iterkeys():
                if k not in fields_to_show:
                    res[k]['selectable'] = False
        return res
