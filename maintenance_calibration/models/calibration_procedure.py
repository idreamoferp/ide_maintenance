from openerp import models, fields, api

class CalibrationCalibrationProcedure(models.Model):
    _name = 'calibration.calibration.procedure'
    _description = _name
    
    def get_compute_types(self):
        return self.env['maintenance.calibration'].get_compute_types()
        
    name = fields.Char('Procedure Name', required=True)
    description = fields.Html('Description')
    test_line_ids = fields.One2many('calibration.calibration.procedure.test', string='Tests to Preform', inverse_name ='procedure_id')
    compute_type = fields.Selection(selection='get_compute_types', default="all")
    
class CalibrationCalibrationTest(models.Model):
    _name = 'calibration.calibration.procedure.test'
    _description = _name
    _order = "sequence asc"
    
    def get_test_types(self):
        return self.env['maintenance.calibration.test'].get_test_types()
        
    name = fields.Char('Name', required=True)
    procedure_id = fields.Many2one('calibration.calibration.procedure', string='Procedure',required=True)
    sequence = fields.Integer(string='Sequence')
    
    target_value = fields.Float('Target Value',required=True)
    target_value_uom = fields.Many2one('uom.uom', 'UoM',required=True, copy=True)
    tolerance = fields.Float('Tolerance',required=True)
    tolerance_uom = fields.Many2one('uom.uom', 'UoM',required=True, copy=True)
    test_type = fields.Selection(selection='get_test_types', string="Calculation Type")
    
   
    def copy_data(self, default=None):
        result = super(CalibrationCalibrationTest, self).copy_data(default)
        for item in result:
            item.pop('procedure_id')
        return result