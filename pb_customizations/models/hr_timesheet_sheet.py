from openerp.osv import fields, osv

class hr_timesheet_sheet(osv.osv):
    _inherit = "hr_timesheet_sheet.sheet"

    def name_get(self, cr, uid, ids, context=None):
        res = []
        for record in self.browse(cr, uid, ids, context=context):
            res.append((record.id, record.employee_id.name))
        return res
