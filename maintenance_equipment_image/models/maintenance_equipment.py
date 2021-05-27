from odoo import api, fields, models


class MaintenanceEquipment(models.Model):
    _inherit = "maintenance.equipment"

    image = fields.Image("Image", attachment=True, max_width=1920, max_height=1920)
    image_128 = fields.Image("Variant Image 128", related="image", max_width=128, max_height=128, store=True)