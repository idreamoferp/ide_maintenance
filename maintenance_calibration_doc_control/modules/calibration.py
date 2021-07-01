from openerp import models, fields, api

class MaintenanceCalibration(models.Model):
    _inherit = 'maintenance.calibration'
    
    description = fields.Related(related='document_page_history_id.content')
    
    #link this to the document page history object of the current verison at the time of the calibration.
    document_page_history_id = fields.Many2one(comodel='document.page.history')
    
class CalibrationCalibrationProcedure(models.Model):
    _inherit = 'calibration.calibration.procedure'
    
    description = fields.Related(related='document_page_id.content')
    
    #link to the document page object that we create on_create here
    document_page_id = fields.Many2one(comodel='document.page')