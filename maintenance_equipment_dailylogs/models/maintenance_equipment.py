from odoo import api, fields, models


class MaintenanceEquipment(models.Model):
    _inherit = "maintenance.equipment"
    
    daily_log_template_ids = fields.Many2many(comodel_name="maintenance.equipment.log.template", string="Log Templates")
    daily_log_ids = fields.One2many("maintenance.equipment.dailylog", "equipment_id", string="Daily Maintenance Logs")
    active_daily_log_id = fields.One2many("maintenance.equipment.dailylog", compute="_compute_active_daily_log")
    
    
    def _compute_active_daily_log(self):
        for item in self:
            item.active_daily_log_id = item.daily_log_ids.filtered(lambda x: x.end_date == False)
            
    def active_daily_log(self):
        return True
  
