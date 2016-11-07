from openerp import models, api, fields

class MailTemplate(models.Model):
    _inherit = 'mail.template'
    
    @api.multi
    def send_mail(self, res_id, force_send=False, raise_exception=False):
        return True