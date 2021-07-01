from odoo import models, fields, api

class MaintenanceCalibration(models.Model):
    _name = 'maintenance.calibration'
    _description = _name
    _order = "calibration_end_date desc"
    
    def get_compute_types(self):
        return [("average","Average"),("all","All Passing")]
        
        
    name = fields.Char('Name')
    equipment_id = fields.Many2one('maintenance.equipment', string='Equipment', required=True)
    calibration_start_date = fields.Datetime('Start Date', track_visibility='onchange')
    calibration_end_date = fields.Datetime('End Date', track_visibility='onchange')
    responsible_user_id = fields.Many2one('res.users', string='Owner', track_visibility='onchange')
    partner_id = fields.Many2one('res.partner', string='Calibrated By')
    calibration_cert = fields.Binary('Calibration Certificate', attachment=True)
    calibration_type = fields.Many2one('maintenance.calibration.type', string='Calibration Type')
    
    #procedure detail...
    procedure_id = fields.Many2one('calibration.calibration.procedure', string='Procedure')
    procedure_version = fields.Integer(string='Procedure Version')
    description = fields.Html('Description')
    test_ids = fields.One2many('maintenance.calibration.test', 'calibration_id', string="Tests")
    compute_type = fields.Selection(selection='get_compute_types', default='all')
    
    #pass fail info
    initial_result = fields.Boolean('As Found Result', compute='compute_results')
    final_result = fields.Boolean('As Left Result', compute='compute_results')
    
    def compute_results(self):
        for item in self:
            item.initial_result = True
            item.final_result = True
            if item.compute_type == 'average':
                len_initial = 0
                len_final = 0
                for test in item.test_ids:
                    if not test.initial_result:
                        len_initial += 1
                    if not test.final_result:
                        len_final += 1
                if (len_initial / len(item.test_ids)) <= 50:
                    item.initial_result = False
                if (len_final / len(item.test_ids)) <= 50:
                    item.final_result = False
                    
                
            if item.compute_type == 'all':
                for test in item.test_ids:
                    if not test.initial_result:
                        item.initial_result = False
                    if not test.final_result:
                        item.final_result = False
                
            
    @api.onchange('procedure_id')
    def on_change_procedure_id(self):
        self.description = ""
        self.name = ""
        self.procedure_version = False
        
        tests = []
        for line in self.test_ids:
            tests.append((2, line.id))
        
        
        
        if len(self.procedure_id):
            self.description = self.procedure_id.description
            self.name = self.procedure_id.name
            #self.procedure_version = self.procedure_id.version
            
            for line in self.procedure_id.test_line_ids:
                test = line.copy_data()[0]
                test['initial_value_uom'] = test['target_value_uom']
                test['final_value_uom'] = test['target_value_uom']
                tests.append((0, 0, test))
                
        self.test_ids = tests
            
class MaintenanceCalibrationType(models.Model):
    _name = 'maintenance.calibration.type'
    _description = _name
    name = fields.Char('Calibration Type', required=True)
    calibration_required = fields.Boolean(string='Calibration Required', default=True)

class MaintenanceCalibrationTest(models.Model):
    _name = 'maintenance.calibration.test'
    _description = _name
    _order = "sequence asc"
    
    def _compute_cal_type(self):
        for item in self:
            item.calibration_type = item.calibration_id.calibration_type
    
    def get_test_types(self):
        return [("tolerance", "In Tolerance"),(">", "Greater than Target"),("<", "Less than Target")]
        
    sequence = fields.Integer(string='Sequence')
    calibration_id = fields.Many2one('maintenance.calibration', string='Calibration')
    calibration_type = fields.Many2one('maintenance.calibration.type', string='Calibration Type', compute='_compute_cal_type')
    name = fields.Char('Name', required=True)
    target_value = fields.Float('Target Value',required=True)
    target_value_uom = fields.Many2one('uom.uom', 'UoM',required=True)
    tolerance = fields.Float('Tolerance',required=True)
    tolerance_uom = fields.Many2one('uom.uom', 'UoM',required=True)
    test_type = fields.Selection(selection='get_test_types', string="Calculation Type")
    
    initial_value = fields.Float('As Found Value')
    initial_value_uom = fields.Many2one('uom.uom', 'UoM')
    initial_result = fields.Boolean('As Found Result', compute='compute_results')
    final_value = fields.Float('As Left Value')
    final_value_uom = fields.Many2one('uom.uom', 'UoM')
    final_result = fields.Boolean('As Left Result', compute='compute_results')
    
    def tolerance_compensation(self, measured_value):
        #method is added for future compensation addon modules
        
        #returns a value to compensate tollerance limits
        return 0
        
    def measured_value_compensation(self, measured_value):
        #method is added for future compensation addon modules
        
        #return a compensated measure value
        return measured_value
    
    def compute_results(self):
        for item in self:
            #clear any past calculations
            item.initial_result = False
            item.final_result = False
            
            #uom conversion all to target value UoM
            initial_value_to_uom = item.initial_value_uom._compute_quantity(qty=item.initial_value, to_unit=item.target_value_uom)
            final_value_to_uom = item.final_value_uom._compute_quantity(qty=item.final_value, to_unit=item.target_value_uom)
            
            if item.test_type == "tolerance":
                #fetch the tolerance and compute it to the target uom
                tolerance_to_uom = item.tolerance_uom._compute_quantity(qty=item.tolerance, to_unit=item.target_value_uom)
                
                #get the tollerance compensation for the target value of the test
                tolerance_compensation = item.tolerance_compensation(item.target_value_uom)
                
               #calculate the upper and lower limits of the test.
                lower_limit = item.target_value - (tolerance_to_uom - tolerance_compensation)
                upper_limit = item.target_value + (tolerance_to_uom + tolerance_compensation)
                
                #compare the measured values to the compensated upper and lower limits.
                if lower_limit <= item.measured_value_compensation(initial_value_to_uom) <= upper_limit:
                    item.initial_result = True
                    
                if lower_limit <= item.measured_value_compensation(final_value_to_uom) <= upper_limit:
                    item.final_result = True
            
            if item.test_type == ">":
                if item.measured_value_compensation(initial_value_to_uom) > item.target_value:
                    item.initial_result = True
                if item.measured_value_compensation(final_value_to_uom) > item.target_value:
                    item.final_result = True
            
            if item.test_type == '<':
                if item.measured_value_compensation(initial_value_to_uom) < item.target_value:
                    item.initial_result = True
                if item.measured_value_compensation(final_value_to_uom) < item.target_value:
                    item.final_result = True
            
    @api.onchange('initial_value')
    def on_change_initial_value(self):
        self.compute_results()
    
    @api.onchange('final_value')
    def on_change_final_value(self):
        self.compute_results()
        
    @api.model
    def create(self, vals):
        return super(MaintenanceCalibrationTest, self).create(vals)