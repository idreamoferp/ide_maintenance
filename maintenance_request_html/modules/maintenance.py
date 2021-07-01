from odoo import models, fields, api, _

class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'
    
    description = fields.Html('Description')