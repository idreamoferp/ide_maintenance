from odoo import api, fields, models


class MaintenanceEquipment(models.Model):
    _inherit = "maintenance.equipment"

    attachment_ids = fields.One2many("maintenance.equipment.attachment", "equipment_id", string="Attachments", ondelete="cascade", track_visibility="onchange")
    
    
class EquipmentAttachment(models.Model):
    _name = "maintenance.equipment.attachment"
    _description = _name
    
    active = fields.Boolean("Active", default=True)
    name = fields.Char("Name", required=True)
    attachment = fields.Binary("Attachment", attachment=True)
    equipment_id = fields.Many2one("maintenance.equipment", "Equipment")