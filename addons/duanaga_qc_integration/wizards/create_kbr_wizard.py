# -*- coding: utf-8 -*-
"""
Wizard: Create QC KBR Decision dari Production Order
Industri flow: QC Analyst input hasil lab di sini
"""

import logging

from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


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

    # QC Spec boundaries — ditampilkan read-only, sumbernya spesifikasi produk.
    ph_min = fields.Float(
        related="product_id.qc_ph_min",
        string="Spec pH Min",
        readonly=True,
    )
    ph_max = fields.Float(
        related="product_id.qc_ph_max",
        string="Spec pH Max",
        readonly=True,
    )
    visc_min = fields.Float(
        related="product_id.qc_visc_min",
        string="Spec Visc Min",
        readonly=True,
    )
    visc_max = fields.Float(
        related="product_id.qc_visc_max",
        string="Spec Visc Max",
        readonly=True,
    )
    spec_version = fields.Char(
        related="product_id.qc_spec_version",
        string="Spec Version",
        readonly=True,
    )

    @api.model
    def _default_production_id(self):
        """Ambil production_id dari context (tombol di form production order)."""
        active_id = self.env.context.get("active_id")
        if not active_id:
            return self.env["mrp.production"]
        return self.env["mrp.production"].browse(active_id).exists()

    def create_and_submit(self):
        """Buat KBR Decision record lalu submit ke inference engine."""
        self.ensure_one()

        if not self.production_id:
            raise UserError(_("Production Order tidak ditemukan."))

        decision = self.env["qc.kbr.decision"].create({
            "production_id": self.production_id.id,
            "ph_level": self.ph_level,
            "viscosity": self.viscosity,
            "state": "submitted",
        })

        try:
            decision.submit_to_kbr()
        except UserError:
            raise
        except Exception as exc:  # pragma: no cover - defensive
            _logger.exception("KBR submission gagal untuk %s", decision.name)
            raise UserError(
                _("Gagal mengirim data ke inference engine. "
                  "Periksa log server untuk detail.")
            ) from exc

        return {
            "type": "ir.actions.act_window",
            "res_model": "qc.kbr.decision",
            "res_id": decision.id,
            "view_mode": "form",
            "target": "current",
        }
