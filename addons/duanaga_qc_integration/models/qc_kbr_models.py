# -*- coding: utf-8 -*-
"""
Models untuk QC KBR Integration
Struktur industri kosmetik:
  - mrp.production    → Production Order (batch manufacturing)
  - quality.check     → QC Test Record (pH, viscosity hasil lab)
  - qc.kbr.decision   → Hasil inference + decision tracking
"""

import logging
import requests
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

# ─── Konfigurasi API ──────────────────────────────────────────────────────────
QC_API_BASE = "http://qc_api:8000"


def call_qc_engine(batch_id: str, ph_level: float, viscosity: float) -> dict:
    """
    Kirim request ke QC Inference Engine.
    Industri pattern: HTTP POST dengan retry + timeout.
    """
    url = f"{QC_API_BASE}/api/qc-check"
    payload = {
        "batch_id": batch_id,
        "ph_level": ph_level,
        "viscosity": viscosity,
    }
    try:
        response = requests.post(
            url,
            json=payload,
            timeout=10,
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        _logger.error(
            f"QC Engine unreachable at {url}. Pastikan service qc_api running."
        )
        raise UserError(
            _("QC Inference Engine tidak dapat dijangkau.\n"
              "Pastikan service 'qc_api' aktif di docker-compose.")
        )
    except requests.exceptions.Timeout:
        _logger.error(f"QC Engine timeout untuk batch {batch_id}")
        raise UserError(_("QC Engine timeout. Coba lagi."))
    except requests.exceptions.HTTPError as e:
        _logger.error(f"QC Engine HTTP error: {e}")
        raise UserError(_(f"QC Engine error: {e}"))


# ─── QC KBR Decision Record ───────────────────────────────────────────────────
class QcKbrDecision(models.Model):
    """
    Record keputusan KBR per batch.
    Industries: traceability log — semua QC decision harus audit trail.
    """
    _name = "qc.kbr.decision"
    _description = "QC KBR Decision Record"
    _order = "create_date desc"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(
        string="Reference",
        default="New",
        readonly=True,
        copy=False,
    )
    production_id = fields.Many2one(
        "mrp.production",
        string="Production Order",
        ondelete="cascade",
        required=True,
    )
    batch_id = fields.Char(
        string="Batch Number",
        compute="_compute_batch_id",
        store=True,
        readonly=True,
    )

    def _compute_batch_id(self):
        for rec in self:
            rec.batch_id = rec.production_id.name
    product_id = fields.Many2one(
        related="production_id.product_id",
        string="Product",
        store=True,
        readonly=True,
    )
    qty_produced = fields.Float(
        related="production_id.qty_produced",
        string="Qty Produced",
        readonly=True,
    )
    qty_approved = fields.Float(
        string="Qty Approved",
        readonly=True,
        copy=False,
    )

    # QC Parameters (input ke engine)
    ph_level = fields.Float(
        string="pH Level",
        digits=(5, 2),
        required=True,
    )
    viscosity = fields.Float(
        string="Viscosity (Pa.s)",
        digits=(5, 3),
        required=True,
    )

    # QC Spec Boundaries (referensi dari quality_control)
    ph_min = fields.Float(default=5.5, string="pH Min")
    ph_max = fields.Float(default=6.5, string="pH Max")
    visc_min = fields.Float(default=1.05, string="Visc Min")
    visc_max = fields.Float(default=1.10, string="Visc Max")

    # Engine Response
    status = fields.Selection([
        ("approved", "Approved"),
        ("rework", "Rework"),
        ("rejected", "Rejected"),
    ], string="QC Status", readonly=True, copy=False)

    recommendation = fields.Text(string="Recommendation", readonly=True)
    ph_in_range = fields.Boolean(string="pH In Range", readonly=True)
    viscosity_in_range = fields.Boolean(string="Viscosity In Range", readonly=True)

    # Audit
    user_id = fields.Many2one(
        "res.users",
        string="QC Analyst",
        default=lambda self: self.env.user,
        readonly=True,
    )
    api_response_raw = fields.Text(
        string="Raw API Response",
        readonly=True,
        help="Debug: raw JSON dari inference engine",
    )
    state = fields.Selection([
        ("draft", "Draft"),
        ("submitted", "Submitted to KBR"),
        ("done", "Decision Received"),
        ("failed", "API Failed"),
    ], default="draft", string="State", readonly=True, copy=False)

    def _prepare_vals_from_engine(self, result: dict) -> dict:
        """Map response engine ke field Odoo."""
        status_map = {
            "Approved": "approved",
            "Rework": "rework",
            "Rejected": "rejected",
        }
        return {
            "status": status_map.get(result.get("status"), False),
            "recommendation": result.get("recommendation", ""),
            "ph_in_range": result.get("ph_in_range", False),
            "viscosity_in_range": result.get("viscosity_in_range", False),
            "api_response_raw": str(result),
            "state": "done",
        }

    def submit_to_kbr(self):
        """
        Aksi utama: kirim QC data ke inference engine.
        Called dari button di form view.

        Industri flow:
          1. QC Analyst input pH + viscosity
          2. Klik "Submit to KBR"
          3. Engine return decision
          4. Status auto-update di Production Order
        """
        for record in self:
            if record.state in ("done", "failed"):
                raise UserError(
                    _("Decision already processed for %s") % record.name
                )

            try:
                result = call_qc_engine(
                    batch_id=record.batch_id or record.production_id.name,
                    ph_level=record.ph_level,
                    viscosity=record.viscosity,
                )
                vals = record._prepare_vals_from_engine(result)
                record.write(vals)

                # Update Production Order state
                record.production_id._update_from_kbr_decision(vals)

                _logger.info(
                    f"KBR Decision: batch={record.batch_id} "
                    f"→ status={vals['status']}"
                )

            except Exception as e:
                record.write({
                    "state": "failed",
                    "recommendation": str(e),
                })
                raise


# ─── Extend mrp.production ────────────────────────────────────────────────────
class MrpProduction(models.Model):
    _inherit = "mrp.production"

    kbr_decision_ids = fields.One2many(
        "qc.kbr.decision",
        "production_id",
        string="KBR Decisions",
        readonly=True,
    )

    kbr_latest_status = fields.Selection([
        ("approved", "Approved"),
        ("rework", "Rework"),
        ("rejected", "Rejected"),
    ], compute="_compute_kbr_status", store=True, string="QC Status")

    qty_approved = fields.Float(
        string="Qty Approved",
        copy=False,
        help="Quantity yang lulus QC",
    )

    def _compute_kbr_status(self):
        for rec in self:
            decisions = rec.kbr_decision_ids.filtered(lambda d: d.state == "done")
            rec.kbr_latest_status = decisions[:1].status or False

    def _update_from_kbr_decision(self, decision_vals: dict):
        """
        Hook: dipanggil setelah KBR decision dibuat.
        Update state production order berdasarkan hasil QC.
        """
        status = decision_vals.get("status")

        if status == "approved":
            self.write({
                "state": "done",
                "qty_approved": self.qty_produced,
            })
            # Log quality pass
            self.env["stock.quant"]._update_available_quantity(
                self.product_id,
                self.location_dest_id,
                self.qty_produced,
            )
            _logger.info(
                f"Batch {self.name} APPROVED. {self.qty_produced} units released."
            )

        elif status == "rework":
            self.write({"state": "confirmed"})  # back to production
            # Kirim notifikasi
            self.message_post(
                body=_(
                    f"<b>QC Rework Required</b><br/>"
                    f"Recommendation: {decision_vals.get('recommendation')}"
                ),
                message_type="notification",
                subtype_xmlid="mail.mt_note",
            )

        elif status == "rejected":
            self.write({
                "state": "cancel",
                "qty_approved": 0.0,
            })
            self.message_post(
                body=_(
                    f"<b>QC Rejected</b><br/>"
                    f"Recommendation: {decision_vals.get('recommendation')}"
                ),
                message_type="notification",
                subtype_xmlid="mail.mt_comment",
            )
