from odoo import models, fields, api
from datetime import date

class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'
    
    def measured_value_compensation(self, measured_value, measured_uom):
        #get the current calibration record for this equipment
        calibration_id = self.calibration_ids.filtered(lambda r: r.calibration_end_date >= date.today() and r.final_result)
        
        #find the upper and lower calibration tests for this measured value
        
        #conver all the tests in the calibration to the measured_uom value, store them in a dict.
        converted_test_ids = {}
        for test in calibration_id.test_ids:
            converted_test_ids[test.final_value_uom._compute_quantity(qty=test.target_value, to_unit=measured_uom)] = test.id
        
        
        upper_test = 0
        lowwer_test = 0
        
        for value in converted_test_ids:
            if measured_value <= value:
                if value >= upper_test:
                    upper_test = converted_test_ids[value]
            
            if measured_value >= value:
                if value <= lowwer_test:
                    lowwer_test = converted_test_ids[value]
            
        #if a upper and lower test could not be found, return the measuired value
        if upper_test == 0 or lowwer_test == 0:
            return measured_value
        
        #fretch the upper and lower calibrations    
        upper_test = self.env['maintenance.calibration.test'].browse(upper_test)
        lowwer_test = self.env['maintenance.calibration.test'].browse(lowwer_test)
        
        x1 = lowwer_test.target_value_uom._compute_quantity(qty=lowwer_test.target_value, to_unit=measured_uom)
        x2 = measured_value
        x3 = upper_test.target_value_uom._compute_quantity(qty=upper_test.target_value, to_unit=measured_uom)
        y1 = lowwer_test.final_value_uom._compute_quantity(qty=lowwer_test.final_value, to_unit=measured_uom)
        y3 = upper_test.final_value_uom._compute_quantity(qty=upper_test.final_value, to_unit=measured_uom)
        
        computed_value = (x2-x1)*(y3-y1)/(x3-x1)+y1
        return computed_value