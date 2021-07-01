from odoo import models, fields, api

class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'
    
    location = fields.Many2one('stock.location', string='Location', track_visibility='onchange', domain="['|',('usage','=','production'),('usage','=','internal'),]")#
