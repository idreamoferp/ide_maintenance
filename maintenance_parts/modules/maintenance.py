from openerp import models, fields, api

class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'
    
    part_ids = fields.Many2many('product.product', string='Parts', help="Parts inventory for this Equipment", copy=True)
    

class MaintenanceRequest(models.Model):
    _name = 'maintenance.request'
    _inherit = ['maintenance.request', 'barcodes.barcode_events_mixin']
   
    part_move_ids = fields.One2many('stock.move', 'maintenance_request_id', 'Parts to Consume', copy=True,)
    reservation_state = fields.Selection([('confirmed', 'Waiting'),('assigned', 'Ready'),('waiting', 'Waiting Another Operation')], string='Material Availability', compute='_compute_state', copy=False, index=True, readonly=True, store=True, tracking=True,)    
    
    @api.depends('part_move_ids')
    def _compute_state(self):
        for item in self:
            item.reservation_state = 'confirmed'

            
        pass

    def on_barcode_scanned(self, barcode):
        product_product = self.env['product.product']
        results = product_product._name_search(name=barcode)
        product_id = False
        if len(results):
            product_id = product_product.browse(results[0][0])
        move = False
        for move_id in self.part_move_ids:
            if move_id.product_id.id == product_id.id and move_id.is_done == False:
                move = move_id
        
        if not move:
            move = self.add_part_to_consume(product_id)

        move.move_line_ids[0].qty_done += 1.0
        move._action_done()
        pass
    
    def prepare_move_line(self):
        vals = {}
        vals['location_id'] = self.env.ref("maintenance_parts.maintenance_parts_location").id
        vals['location_dest_id'] = self.env.ref("maintenance_parts.maintenance_parts_consumed").id
        vals['maintenance_request_id'] = self.id
        vals['name'] = self.name
        vals['procure_method'] = 'make_to_stock'
        vals['date_expected'] = self.schedule_date or fields.Date.today()
        return vals

    def add_part_to_consume(self, product_id, qty=1):
        new_parts_move = self.prepare_move_line()
        new_parts_move['product_id'] = product_id.id
        new_parts_move['product_uom'] = product_id.uom_id.id
        new_parts_move['product_uom_qty'] = float(qty)
        new_move = self.env['stock.move'].create(new_parts_move)
        new_move._action_confirm()
        new_move._action_assign()
        return new_move

    def action_assign_parts(self):  
        for part in self.part_move_ids:
            part._action_assign()
 
    def action_mark_parts_done(self):
        for part in self.part_move_ids:
            part._action_done()

    

    

class StockMove(models.Model):
    _inherit = 'stock.move'
    
    maintenance_request_id = fields.Many2one('maintenance.request', 'Maintenance Request for materials')
        
class ProductTemplate(models.Model):
    _inherit = "product.template"
    
    #type = fields.Selection(selection_add=[('parts', 'Maintenance Parts')])