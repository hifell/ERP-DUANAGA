from odoo import models, fields

class StockLocation(models.Model):
    _inherit = 'stock.location'
    is_consignment = fields.Boolean(string='Consignment Location', default=False)
    consignment_owner_id = fields.Many2one('res.partner', string='Consignment Owner')

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    is_consignment = fields.Boolean(string='Consignment / Toll', default=False)
    consignment_owner_id = fields.Many2one('res.partner', string='Owner (Client)')
