from openerp import models, api, fields
from openerp import SUPERUSER_ID

class ResUsers(models.Model):
    _inherit = 'res.users'
    
    email = fields.Char(default='example@patban.com')
    
    def _get_group(self, cr, uid, context=None):
        dataobj = self.pool.get('ir.model.data')
        result = []
        try:
            dummy, group_id = dataobj.get_object_reference(cr, SUPERUSER_ID, 'base', 'group_user')
            result.append(group_id)
            dummy,group_id = dataobj.get_object_reference(cr, SUPERUSER_ID, 'base', 'group_partner_manager')
            result.append(group_id)
            dummy,group_id = dataobj.get_object_reference(cr, SUPERUSER_ID, 'project', 'group_project_user')
            result.append(group_id)
            dummy,group_id = dataobj.get_object_reference(cr, SUPERUSER_ID, 'account', 'group_account_invoice')
            result.append(group_id)
            dummy,group_id = dataobj.get_object_reference(cr, SUPERUSER_ID, 'base', 'group_hr_user')
            result.append(group_id)
        except ValueError:
            # If these groups does not exists anymore
            pass
        return result
    
    def on_change_login(self, cr, uid, ids, login, context=None):
        return {}
    
    _defaults = {
        'groups_id': _get_group,
    }
    
    def create(self, cr, uid, vals, context=None):
        return super(ResUsers, self).create(cr, SUPERUSER_ID, vals, context=context)
    
    def write(self, cr, uid, ids, values, context=None):
        return super(ResUsers, self).write(cr, SUPERUSER_ID, ids, values, context=context)
        
    def unlink(self, cr, uid, ids, context=None):
        return super(ResUsers, self).unlink(cr, SUPERUSER_ID, ids, context=context)