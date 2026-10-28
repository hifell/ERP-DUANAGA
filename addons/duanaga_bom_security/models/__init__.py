from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    material_code = fields.Char(string='Material Code', index=True)
    is_confidential_material = fields.Boolean(string='Confidential Material', default=False)

class MrpBom(models.Model):
    _inherit = 'mrp.bom'
    is_confidential = fields.Boolean(string='Confidential Formula', default=False)
    formula_code = fields.Char(string='Formula Code', index=True)
