from openerp import models, fields, api

class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'
    
    equipment_id = fields.Many2one('maintenance.equipment', string='Equipment', compute='_compute_equiptment_id', inverse="_store_equiptment_id")
    equipment_ids = fields.Many2many('maintenance.equipment', string='Equipments')
    
    def _compute_equiptment_id(self):
        for item in self:
            if len(item.equipment_ids):
                item.equipment_id = item.equipment_ids[0].id
                
    def _store_equiptment_id(self):
        for item in self:
            item.equipment_ids = [(4, item.equipment_id.id)]

class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'
    
    maintenance_ids = fields.Many2many('maintenance.request', string="Maintenance Requests")