from openerp import models, api, fields

class Vehicles(models.Model):
    _name = 'vehicle.vehicle'
    
    name = fields.Char(string="Vehicle Name")
    vehicle_number = fields.Char(string="Vehicle Number")
    rates_per_hr = fields.Char(string="Rates Per Hour")
    
    @api.model
    def fields_get(self, *args, **kwargs):
        fields_to_show = ['name', 'vehicle_number']
        res = super(Vehicles, self.sudo()).fields_get(*args, **kwargs)
        for k in res.iterkeys():
                if k not in fields_to_show:
                    res[k]['selectable'] = False
        return res
