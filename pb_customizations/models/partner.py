from openerp import models, api, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    @api.multi
    def _get_default_country(self):
        return self.env['res.country'].search([('code', '=', 'AI')], limit=1).id
    
    country_id = fields.Many2one(default=_get_default_country)
    opt_out = fields.Boolean(default=True)
    notify_email = fields.Selection(default='none')
    zip = fields.Char(default='AI-2640')
    mobile = fields.Char(default='+1 264')
    state_id = fields.Many2one()
    po_box = fields.Char()
    company_type = fields.Selection(default='company')
    type = fields.Selection(default='invoice')
    
    @api.model
    def fields_get(self, *args, **kwargs):
        fields_to_show = ['name', 'mobile', 'email']
        res = super(ResPartner, self.sudo()).fields_get(*args, **kwargs)
        for k in res.iterkeys():
                if k not in fields_to_show:
                    res[k]['selectable'] = False
        return res
