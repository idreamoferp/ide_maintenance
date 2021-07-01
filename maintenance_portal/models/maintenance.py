from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError

# class MrpBom(models.Model):
#     _inherit = 'mrp.bom'
    
#     @api.multi
#     def name_get(self):
#         return [(bom.id, '%s%s' % (bom.code and '%s: ' % bom.code or '', bom.product_id.display_name or bom.product_tmpl_id.display_name)) for bom in self]
    
    # @api.constrains('product_id', 'product_tmpl_id', 'bom_line_ids')
    # def _check_product_recursion(self):
    #     for bom in self:
    #         for bom_line in bom.bom_line_ids:
    #             product_bom_id = self._bom_find(product=bom_line.product_id).id
    #             if product_bom_id == bom.id:
    #                 raise ValidationError(_('BoM line product %s should not be same as BoM product.') % bom.display_name)