from openerp import models, api, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    opt_out = fields.Boolean(default=True)
    notify_email = fields.Selection(default='none')
    zip = fields.Char(related='state_id.code')
