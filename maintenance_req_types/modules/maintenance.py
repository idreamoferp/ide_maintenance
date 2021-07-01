from odoo import models, fields, api

class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'
    
    maintenance_type_id = fields.Many2one('maintenance.request.type', string='Maintenance Type')
    

class MaintenanceRequestType(models.Model):
    _name = 'maintenance.request.type'
    _order = "sequence asc"
    
    name = fields.Char('Request Type', required=True)
    corrective = fields.Boolean(string='Type is Corrective', default=True)
    sequence = fields.Integer(string='Sequence')