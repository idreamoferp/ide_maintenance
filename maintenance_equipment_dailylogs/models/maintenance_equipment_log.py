from odoo import api, fields, models

class MaintenanceEquipmentlogs(models.Model):
    _name="maintenance.equipment.dailylog"
    _description=_name
    
    name=fields.Char(string="Name", compute="_compute_name")
    equipment_id=fields.Many2one("maintenance.equipment","Equipment")
    start_date=fields.Datetime(string="Start Date")
    end_date=fields.Datetime(string="End Date")
    start_user_id=fields.Many2one("res.users", string="Startup Operator")
    end_user_id=fields.Many2one("res.users", string="Shutdown Operator")
    startup_line_ids=fields.One2many(comodel_name="maintenance.equipment.dailylog.lineitems", inverse_name="startup_log_id")
    shutdown_line_ids=fields.One2many(comodel_name="maintenance.equipment.dailylog.lineitems", inverse_name="shutdown_log_id")
    template_id = fields.Many2one("maintenance.equipment.log.template", string="Daily Log Template")
    
    def _compute_name(self):
        for item in self:
            item.name = "%s - %s" % (item.equipment_id.name, item.start_date)
    
class MaintenanceEquipmentloglines(models.Model):
    _name="maintenance.equipment.dailylog.lineitems"
    _description=_name
    
    startup_log_id=fields.Many2one("maintenance.equipment.dailylog", copy=False)
    shutdown_log_id=fields.Many2one("maintenance.equipment.dailylog", copy=False)
    title=fields.Char(string="Title")
    description=fields.Html(string="description")
    completed=fields.Boolean(string="Completed",default=False)
    
class MaintenanceEquipmentlogTemplate(models.Model):
    _name="maintenance.equipment.log.template"
    _description=_name
    
    name=fields.Char(string="Name")
    startup_line_ids=fields.One2many(comodel_name="maintenance.equipment.dailylog.lineitems", inverse_name="startup_log_id")
    shutdown_line_ids=fields.One2many(comodel_name="maintenance.equipment.dailylog.lineitems", inverse_name="shutdown_log_id")
    
    def _compute_name(self):
        for item in self:
            item.name = "%s - %s" % (item.equipment_id.name, item.start_date)
            
    def create_log_from_template(self):
        vals = {}
        vals['template_id'] = self.id
        
        start_lines = []
        for line in self.startup_line_ids:
            start_lines.append((0,0, line.copy_data()[0]))
            
            
        vals['startup_line_ids'] = start_lines #self.startup_line_ids.copy_data()
        #vals['shutdown_line_ids'] = self.shutdown_line_ids.copy_data()
        if self.env.context.get("equipment_id", False):
            vals['equipment_id'] = self.env.context.get("equipment_id", False)
            
        self.env['maintenance.equipment.dailylog'].create(vals)
        
        return True
        