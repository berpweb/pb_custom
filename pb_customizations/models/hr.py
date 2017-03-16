from openerp import models, api, fields
from openerp.exceptions import ValidationError
from datetime import datetime
from openerp.exceptions import UserError
from datetime_utilities import valid_date, compute_hours_mins

class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    
    user_id_rel = fields.Char(compute='compute_user_id', store=True)
    
    @api.one
    @api.depends('user_id')
    def compute_user_id(self):
        self.user_id_rel = self.user_id.id
            
    @api.one
    @api.constrains('user_id_rel')
    def _check_user_for_emp(self):
        if self.user_id and self.search([('user_id', '=', self.user_id.id), ('id', '!=', self.id)]).ids:
            raise ValidationError('You cannot assign same user to multiple employees.')
        
    @api.model
    def fields_get(self, *args, **kwargs):
        fields_to_show = ['name', 'mobile_phone', 'work_email']
        res = super(HrEmployee, self.sudo()).fields_get(*args, **kwargs)
        for k in res.iterkeys():
                if k not in fields_to_show:
                    res[k]['selectable'] = False
        return res
    
    @api.multi
    def write(self, vals):
        if 'active' in vals and self.user_id:
            self.user_id.active = vals['active']
        return super(HrEmployee, self).write(vals)


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'
    
    emp_id_rel = fields.Char(compute='compute_emp_id', store=True)
    punch_out_address = fields.Char(string="Punch Out Location")
    view_date = fields.Char(compute='_get_attendace_date', store=True, string="Date")
    view_out_time = fields.Char(compute='_get_attendace_date', store=True, string="Punch Out Time")
    update_value = fields.Char(string="Update Value", copy=False)
    change_date_value = fields.Char(string="Update Value", copy=False)
    change_date = fields.Selection([('change_date', 'Change Date?')], default='change_date', string="Change Date?")
    to_update = fields.Selection([('in', 'Punch In'), ('out', 'Punch Out')], default='in')
    location_value = fields.Char(string="Enter location", copy=False)
    location_type = fields.Selection([('in', 'Punch In?'), ('out', 'Punch Out?')], default='in', string="Location type?")
    
    def _altern_si_so(self, cr, uid, ids, context=None):
        return True
    
    _constraints = [(_altern_si_so, 'Error ! Sign in (resp. Sign out) must follow Sign out (resp. Sign in)', ['action'])]

    @api.model
    def fields_get(self, *args, **kwargs):
        fields_to_show = ['employee_id']
        res = super(HrAttendance, self.sudo()).fields_get(*args, **kwargs)
        for k in res.iterkeys():
                if k not in fields_to_show:
                    res[k]['selectable'] = False
        return res
    
    @api.multi
    @api.onchange('update_value')
    def on_change_update_value(self):
        if self.update_value and not valid_date(self.update_value, '%I:%M:%S %p'):
            self.update_value = False
            return {'warning': {
                        'title': 'Error!',
                        'message': 'Please enter the correct format!'}}
            
    @api.multi
    def update_data(self):
        if self.to_update == 'in':
            duration = compute_hours_mins(self.update_value, self.view_out_time, '%I:%M:%S %p')
            params = (duration, self.update_value, self.id)
            sql_query = 'UPDATE hr_attendance SET view_hours = %s , view_in_time = %s WHERE id = %s'
            self.env.cr.execute(sql_query, params)
        elif self.to_update == 'out':
            duration = compute_hours_mins(self.view_in_time, self.update_value, '%I:%M:%S %p')
            params = (duration, self.update_value, self.id)
            sql_query = 'UPDATE hr_attendance SET view_hours = %s , view_out_time = %s WHERE id = %s'
            self.env.cr.execute(sql_query, params)
        else:
            self.update_value = False
            raise UserError('Please select punch in/out to update!')

    @api.multi
    @api.onchange('change_date_value')
    def on_change_change_date_value(self):
        if self.change_date_value and not valid_date(self.change_date_value, '%m/%d/%Y'):
            self.change_date_value = False
            return {'warning': {
                'title': 'Error!',
                'message': 'Please enter the correct format!'}}

    @api.multi
    def update_date_value(self):
        if self.change_date == 'change_date':
            params = (self.change_date_value, self.id)
            sql_query = 'UPDATE hr_attendance SET view_date = %s WHERE id = %s'
            self.env.cr.execute(sql_query, params)
        else:
            self.change_date_value = False
            raise UserError('Please select change date to update!')

    @api.multi
    def update_location(self):
        if self.location_type == 'in':
            params = (self.location_value, self.id)
            sql_query = 'UPDATE hr_attendance SET punch_in_address = %s WHERE id = %s'
            self.env.cr.execute(sql_query, params)
        elif self.location_type == 'out':
            params = (self.location_value, self.id)
            sql_query = 'UPDATE hr_attendance SET punch_out_address = %s WHERE id = %s'
            self.env.cr.execute(sql_query, params)
        else:
            self.location_value = False
            raise UserError('Please select location type to update!')
    
    @api.one
    @api.depends('employee_id')
    def compute_emp_id(self):
        self.emp_id_rel = self.employee_id.id
            
    @api.model
    def create(self, vals):
        if vals.get('employee_id', False):
            vals['employee_id'] = int(vals['employee_id'])
        return super(HrAttendance, self.sudo()).create(vals)
    
    @api.one
    @api.depends('name')
    def _get_attendace_date(self):
        if self.name:
            d = datetime.strptime(self.name, '%Y-%m-%d %H:%M:%S')
            day_string = d.strftime('%m/%d/%Y')
            time_string = d.strftime('%I:%M:%S %p')
            self.view_date = day_string
            self.view_out_time = time_string
    