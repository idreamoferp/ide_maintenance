from odoo import models, fields, api

class MaintenanceCalibrationTest(models.Model):
    _inherit = 'maintenance.calibration.test'
    
    uncertainty_value = fields.Float('Uncertainty Value')
    uncertainty_value_uom = fields.Many2one('uom.uom', 'UoM')