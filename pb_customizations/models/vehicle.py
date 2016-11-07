from openerp import models, api, fields

class Vehicles(models.Model):
    _name = 'vehicle.vehicle'
    
    name = fields.Char(string="Vehicle Name")
    vehicle_number = fields.Char(string="Vehicle Number")
