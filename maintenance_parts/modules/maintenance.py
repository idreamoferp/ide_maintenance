from openerp import models, fields, api

class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'
    
    part_ids = fields.Many2many('product.product', string='Parts', copy=True)
    

class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'
    
    move_raw_ids = fields.One2many('stock.move', 'maintenance_request_id', 'Parts to Consume', copy=True,)
        
class StockMove(models.Model):
    _inherit = 'stock.move'
    
    maintenance_request_id = fields.Many2one('maintenance.request', 'Maintenance Request for materials')
        
class ProductTemplate(models.Model):
    _inherit = "product.template"
    
    #type = fields.Selection(selection_add=[('parts', 'Maintenance Parts')])