from odoo import models, fields, api

class MaintenanceCalibrationTest(models.Model):
    _inherit = 'maintenance.calibration.test'
    
    test_equipment_id = fields.Many2one('maintenance.equipment', string='Test Equipment')
    
        
    def measured_value_compensation(self, measured_value):
        #if no test equipment on record, do not attpemt compensation.
        if not len(self.test_equipment_id):
            return measured_value
            
        return self.test_equipment_id.measured_value_compensation(measured_value, self.target_value_uom)
    
    
    @api.onchange('test_equipment_id')
    def on_change_test_equipment(self):
        #check calibration status
        verification = self.verify_test_equipment_calibration()
        if not verification:
            self.test_equipment_id=False

    def verify_test_equipment_calibration(self, test_equipment_id=None):
        if not test_equipment_id:
            test_equipment_id = self.test_equipment_id
        
        #check if the test equipment is calibrated
        if not test_equipment_id.calibrated:
            return False
        
        #check if the test equpiment is calibrated to measure UoM in this test category
        uom_in_this_group = self.env['uom.uom'].search([("category_id","=",self.target_value_uom.category_id.id)]).ids
        
        #cycle through all the test equpiment calibration tests for a uom that is in the same category
        for test_line in test_equipment_id.calibration_ids[0].test_ids:
            if not test_line.target_value_uom.id in uom_in_this_group:
                return False
                
        return True
                
    
        
    