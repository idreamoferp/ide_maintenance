from odoo import models, fields
from datetime import datetime

class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'
    
    def _compute_calibration_status(self):
        for item in self:
            if item.calibration_type.calibration_required == False:
                item.calibration_status = 'Not Subject to Calibration'
                item.calibrated = False
                return
            
            if len(item.calibration_ids) == 0:
                item.calibration_status = 'Not Calibrated'
                item.calibrated = False
                return
            
            if len(item.calibration_ids):
                calibrations = item.calibration_ids.filtered(lambda r: r.calibration_end_date >= datetime.now())
                if len(calibrations):
                    if item.calibration_ids[0].final_result:
                        item.calibration_status = 'Calibrated'
                        item.calibrated = True
                        return
                    if not item.calibration_ids[0].final_result:
                        item.calibration_status = 'Out of Tolerance'
                        item.calibrated = False
                        return
            
            item.calibration_status = 'Expired'
            item.calibrated = False
        
    calibration_ids = fields.One2many('maintenance.calibration', 'equipment_id', string="Calibrations")
    calibration_type = fields.Many2one('maintenance.calibration.type', string='Calibration Type', track_visibility='onchange')
    calibration_status = fields.Text(string="Calibration Status", compute='_compute_calibration_status')
    calibrated = fields.Boolean('Calibrated', compute='_compute_calibration_status')
    
    calibration_interval = fields.Integer('Calibration Interval', default=1)
    calibration_interval_type = fields.Selection([('minutes', 'Minutes'),('hours', 'Hours'),('work_days', 'Work Days'),('days', 'Days'),('weeks', 'Weeks'),('months', 'Months'),('year', 'Years')], string='Interval Unit', default="year")
    calibration_procedure_id = fields.Many2one('calibration.calibration.procedure', string='Calibration Procedure', track_visibility='onchange')