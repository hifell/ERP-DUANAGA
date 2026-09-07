# -*- coding: utf-8 -*-
"""
Wizard: Create QC KBR Decision dari Production Order
Industri flow: QC Analyst input hasil lab di sini
"""

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class CreateKbrDecisionWizard(models.TransientModel):
    _name = "create.kbr.decision.wizard"
    _description = "Create KBR Decision Wizard"

    production_id = fields.Many2one(
        "mrp.production",
        string="Production Order",
        required=True,
        readonly=True,
        default=lambda self: self._default_production_id(),
    )
    batch_id = fields.Char(
        related="production_id.name",
        string="Batch Number",
        readonly=True,
    )
    product_id = fields.Many2one(
        related="production_id.product_id",
        string="Product",
        readonly=True,
    )
    qty_produced = fields.Float(
        related="production_id.qty_produced",
        string="Qty Produced",
        readonly=True,
    )

    # QC Lab Input
    ph_level = fields.Float(
        string="pH Level (Lab Result)",
        digits=(5, 2),
        required=True,
        help="Hasil pengukuran pH dari Quality Control lab",
    )
    viscosity = fields.Float(
        string="Viscosity (Pa.s)",
        digits=(5, 3),
        required=True,
        help="Hasil pengukuran viskositas dari Quality Control lab",
    )

    # QC Spec boundaries (bisa di-configure per product)
    ph_min = fields.Float(default=5.5, string="Spec pH Min")
    ph_max = fields.Float(default=6.5, string="Spec pH Max")
    visc_min = fields.Float(default=1.05, string="Spec Visc Min")
    visc_max = fields.Float(default=1.10, string="Spec Visc Max")

    def _default_production_id(self):
        """Ambil production_id dari context (tombol di form production order)."""
        active_id = self.env.context.get("active_id")
        return active_id

    def create_and_submit(self):
        """
        Buat KBR Decision record, langsung submit ke inference engine.
        Pattern industri: wizard → create record → call engine → return result.
        """
        self.ensure_one()

        # 1. Create decision record
        decision = self.env["qc.kbr.decision"].create({
            "production_id": self.production_id.id,
            "ph_level": self.ph_level,
            "viscosity": self.viscosity,
            "ph_min": self.ph_min,
            "ph_max": self.ph_max,
            "visc_min": self.visc_min,
            "visc_max": self.visc_max,
            "state": "submitted",
        })

        # 2. Submit ke inference engine
        try:
            decision.submit_to_kbr()
        except Exception as e:
            # Error sudah di-log di model, tetap return wizard result
            _logger = self.env.registry["qc.kbr.decision"].__logger__
            _logger.warning(f"KBR submission failed: {e}")

        # 3. Return view ke decision record
        return {
            "type": "ir.actions.act_window",
            "res_model": "qc.kbr.decision",
            "res_id": decision.id,
            "view_mode": "form",
            "target": "current",
        }
