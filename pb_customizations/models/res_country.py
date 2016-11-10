from openerp import models, api, fields

class CountryState(models.Model):
    _inherit = 'res.country.state'
    
    @api.multi
    def _get_default_country(self):
        return self.env['res.country'].search([('code', '=', 'AI')], limit=1).id
    
    country_id = fields.Many2one(default=_get_default_country)
    