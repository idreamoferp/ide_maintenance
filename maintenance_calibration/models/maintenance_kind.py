from odoo import fields, models

class MaintenanceKind(models.Model):

    _inherit = "maintenance.kind"
    calibration = fields.Boolean(string='Type is Calibration', default=False)