from datetime import datetime

from openerp.osv import fields, osv

class hr_attendance(osv.osv):
    _inherit = "hr.attendance"

    def _worked_hours_compute(self, cr, uid, ids, fieldnames, args, context=None):
        """For each hr.attendance record of action sign-in: assign 0.
        For each hr.attendance record of action sign-out: assign number of hours since last sign-in.
        """
        res = {}
        for obj in self.browse(cr, uid, ids, context=context):
            hours_data = {'punch_in_time': False, 'worked_hours': False}
            if obj.action == 'sign_in':
                res[obj.id] = hours_data
            elif obj.action == 'sign_out':
                # Get the associated sign-in
                last_signin_id = self.search(cr, uid, [
                    ('employee_id', '=', obj.employee_id.id),
                    ('name', '<', obj.name), ('action', '=', 'sign_in')
                ], limit=1, order='name DESC')
                if last_signin_id:
                    last_signin = self.browse(cr, uid, last_signin_id, context=context)[0]

                    # Compute time elapsed between sign-in and sign-out
                    last_signin_datetime = datetime.strptime(last_signin.name, '%Y-%m-%d %H:%M:%S')
                    signout_datetime = datetime.strptime(obj.name, '%Y-%m-%d %H:%M:%S')
                    workedhours_datetime = (signout_datetime - last_signin_datetime)
                    hours = workedhours_datetime.seconds/(60 * 60)
                    minutes = (workedhours_datetime.seconds/(60)) % 60
                    view_in_time = last_signin_datetime.strftime('%H:%M:%S')
                    hours_data = {'punch_in_time': last_signin_datetime, 
                                  'view_in_time': view_in_time,
                                  'worked_hours': ((workedhours_datetime.seconds) / 60) / 60.0,
                                  'view_hours': '%s:%s'%(hours,minutes),
                                  'punch_in_id': last_signin,
                                  'punch_in_address': last_signin.punch_out_address}
                    res[obj.id] = hours_data
                else:
                    res[obj.id] = hours_data
        return res

    _columns = {
        'punch_in_time': fields.function(_worked_hours_compute, type='datetime', string='Punch In Time', store=True, multi='work'),
        'view_in_time': fields.function(_worked_hours_compute, type='char', string='Punch In Time', store=True, multi='work'),
        'punch_in_address': fields.function(_worked_hours_compute, type='char', string='Punch In Location', store=True, multi='work'),
        'punch_in_id': fields.function(_worked_hours_compute, type='integer', string='Previous Punch In ID', store=True, multi='work'),
        'worked_hours': fields.function(_worked_hours_compute, type='float', string='Worked Hours', store=True, multi='work'),
        'view_hours': fields.function(_worked_hours_compute, type='char', string='Hours', store=True, multi='work'),
    }


# from openerp import models, api
# from openerp.exceptions import UserError
# 
# class HrAttendance(models.Model):
#     _inherit = "hr.attendance"
#     
#     @api.onchange('view_hours')
#     def on_change_view_hours(self):
#         if self.view_hours and '.' in str(self.view_hours):
#             raise UserError('Please use colon ":" instead of dot "." in attendance hours!')
#         try:
#             self.view_hours.split(':')[1] if self.view_hours else '0:0'
#         except IndexError:
#             self.view_hours = "%s:%s"%(self.view_hours.split(':')[0], 0)
#         else:
#             pass
#         
#     @api.multi
#     def write(self, vals):
#         if vals.get('view_hours', False) and '.' in vals['view_hours']:
#             raise UserError('Please use colon ":" instead of dot "." in attendance hours!')
