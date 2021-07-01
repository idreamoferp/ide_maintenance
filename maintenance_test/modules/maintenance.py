from openerp import models, fields, api

class MaintenanceTest(models.Model):
    _name = 'maintenance.test'
    
    name = fields.Char('Name', required=True)
    equipment_id = fields.Many2one('maintenance.equipment', string='Equipment', )
    request_id = fields.Many2one('maintenance.request', string='Maintenance Request',)
    test_date = fields.Date('Test Date')
    technician_user_id = fields.Many2one('res.users', string='Technician',)
    
    target_value = fields.Float('Target Value')
    target_value_uom = fields.Many2one('product.uom', 'UoM')
    tolerance = fields.Float('Tolerance')
    tolerance_uom = fields.Many2one('product.uom', 'UoM')
    initial_value = fields.Float('Initial Value')
    initial_value_uom = fields.Many2one('product.uom', 'UoM')
    initial_result = fields.Boolean('Initial Result')
    final_value = fields.Float('Final Value')
    final_value_uom = fields.Many2one('product.uom', 'UoM')
    final_result = fields.Boolean('Final Result')
    
    
    @api.onchange('target_value_uom')
    def _onchange_target_value_uom(self):
        self.tolerance_uom = self.target_value_uom
        self.initial_value_uom = self.target_value_uom
        self.final_value_uom = self.target_value_uom
        
    @api.onchange('initial_value', 'final_value', 'target_value', 'tolerance')
    def _onchange_target_value_uom(self):
        self.check_results()
        
    @api.multi
    def write(self, vals):
        return super(MaintenanceTest, self).write(vals)
        
    @api.multi
    def check_results(self):
        for item in self:
            uom_tollerance = item.tolerance_uom._compute_quantity(qty=item.tolerance, to_unit=item.target_value_uom)
            lower_limit = item.target_value - uom_tollerance
            upper_limit = item.target_value + uom_tollerance
            
            uom_initial = item.initial_value_uom._compute_quantity(qty=item.initial_value, to_unit=item.target_value_uom)
            if lower_limit <= uom_initial <= upper_limit:
                item.initial_result = True
            else:
                item.initial_result = False
                
            uom_final = item.final_value_uom._compute_quantity(qty=item.final_value, to_unit=item.target_value_uom)
            if lower_limit <= uom_final <= upper_limit:
                item.final_result = True
            else:
                item.final_result = False
    
    @api.multi
    def copy_data(self, default={}):
        default.update({'initial_value':0, 'final_value':0, 'test_date':False, 'technician_user_id':False})
        return super(MaintenanceTest, self).copy_data(default)
        
class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'
    
    test_ids = fields.One2many('maintenance.test', 'request_id', copy=True)
    
    #on copy data i.e. scheduler copy_data, create new tests for that new WO
    @api.multi
    def copy_data(self, default=None):
        for item in self:
            new_tests = []
            for test in item.test_ids:
                new_tests.append( (0, 0, test.copy_data()) )
                
            default = {'test_ids':new_tests}
        return super(MaintenanceRequest, self).copy_data(default)
        
    @api.multi
    def write(self, vals):
        if vals.get('stage_id'):
            if self.env['maintenance.stage'].browse(vals.get('stage_id')).done:
                self.test_ids.write({'test_date':fields.Date.today()})
                
class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'
    
    test_ids = fields.One2many('maintenance.test', 'equipment_id')