# -*- coding: utf-8 -*-
"""
Models untuk QC KBR Integration.

Struktur industri kosmetik:
  - mrp.production    → Production Order (batch manufacturing)
  - qc.kbr.decision   → Hasil inference + decision tracking
  - product.template  → spesifikasi QC per produk (source of truth)

Keputusan QC adalah keputusan backend: batch yang belum released tidak boleh
keluar lewat delivery order biasa.
"""

import logging
import time

import requests

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

QC_API_BASE = "http://qc_api:8000"
QC_API_KEY_HEADER = "X-Api-Key"
QC_ENGINE_RETRIES = 3
QC_ENGINE_BACKOFF_SECONDS = 2


def call_qc_engine(
    batch_id: str,
    ph_level: float,
    viscosity: float,
    spec: dict | None = None,
    api_key: str | None = None,
) -> dict:
    """Kirim data QC ke inference engine.

    Retry dibatasi supaya batch yang gagal tidak menggantung di UI, dan pesan
    error ke user tidak membocorkan detail internal.
    """
    url = f"{QC_API_BASE}/api/qc-check"
    payload = {
        "batch_id": batch_id,
        "ph_level": ph_level,
        "viscosity": viscosity,
    }
    if spec:
        payload["spec"] = spec

    headers = {"Content-Type": "application/json"}
    if api_key:
        headers[QC_API_KEY_HEADER] = api_key

    last_error = None
    for attempt in range(1, QC_ENGINE_RETRIES + 1):
        try:
            response = requests.post(url, json=payload, timeout=10, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout as exc:
            last_error = exc
            _logger.warning(
                "QC Engine timeout (attempt %s/%s) untuk batch %s",
                attempt, QC_ENGINE_RETRIES, batch_id,
            )
        except requests.exceptions.ConnectionError as exc:
            last_error = exc
            _logger.warning(
                "QC Engine tidak dapat dijangkau (attempt %s/%s) di %s",
                attempt, QC_ENGINE_RETRIES, url,
            )
        except requests.exceptions.HTTPError as exc:
            _logger.error("QC Engine HTTP error: %s", exc)
            raise UserError(
                _("Inference engine menolak permintaan QC (HTTP error).")
            ) from exc

        if attempt < QC_ENGINE_RETRIES:
            time.sleep(QC_ENGINE_BACKOFF_SECONDS * attempt)

    raise UserError(
        _("Inference engine tidak dapat dijangkau setelah %s percobaan. "
          "Pastikan service 'qc_api' aktif dan dapat diakses dari Odoo.")
        % QC_ENGINE_RETRIES
    ) from last_error


class ProductTemplate(models.Model):
    """Spesifikasi QC per produk.

    Nilai default hanya placeholder. Specifications harus divalidasi per
    produk sebelum dipakai untuk keputusan QC.
    """

    _inherit = "product.template"

    qc_ph_min = fields.Float(string="QC pH Min", digits=(5, 2), default=5.5)
    qc_ph_max = fields.Float(string="QC pH Max", digits=(5, 2), default=6.5)
    qc_visc_min = fields.Float(string="QC Visc Min", digits=(5, 3), default=1.05)
    qc_visc_max = fields.Float(string="QC Visc Max", digits=(5, 3), default=1.10)
    qc_spec_version = fields.Char(
        string="QC Spec Version",
        default="DEFAULT-UNVALIDATED",
        help="Versi dokumen spesifikasi yang berlaku untuk produk ini.",
    )
    qc_spec_validated = fields.Boolean(
        string="QC Spec Validated",
        default=False,
        help="Centang setelah spesifikasi produk diverifikasi oleh QA. "
             "Produk tanpa spesifikasi tervalidasi tidak boleh dilepas.",
    )


class QcKbrDecision(models.Model):
    """Record keputusan KBR per batch."""

    _name = "qc.kbr.decision"
    _description = "QC KBR Decision Record"
    _order = "create_date desc, id desc"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(
        string="Reference",
        default=lambda self: _("New"),
        readonly=True,
        copy=False,
        index=True,
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
    lot_id = fields.Many2one(
        "stock.lot",
        string="Lot",
        readonly=True,
        help="Lot dari produk jadi yang diuji.",
    )

    @api.depends("production_id")
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

    # QC Spec Boundaries (disalin dari produk, dipakai saat memanggil engine)
    ph_min = fields.Float(string="pH Min", digits=(5, 2), readonly=True)
    ph_max = fields.Float(string="pH Max", digits=(5, 2), readonly=True)
    visc_min = fields.Float(string="Visc Min", digits=(5, 3), readonly=True)
    visc_max = fields.Float(string="Visc Max", digits=(5, 3), readonly=True)
    spec_version = fields.Char(string="Spec Version", readonly=True)

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

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", _("New")) == _("New"):
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    "qc.kbr.decision"
                ) or _("New")
        return super().create(vals_list)

    @api.constrains("ph_level", "viscosity")
    def _check_measurements(self):
        for rec in self:
            if not 0.0 <= rec.ph_level <= 14.0:
                raise ValidationError(
                    _("pH harus antara 0 dan 14 (terbaca %s).") % rec.ph_level
                )
            if rec.viscosity < 0.0:
                raise ValidationError(
                    _("Viskositas tidak boleh negatif (terbaca %s).")
                    % rec.viscosity
                )

    @api.constrains("ph_min", "ph_max", "visc_min", "visc_max")
    def _check_spec_bounds(self):
        for rec in self:
            if rec.ph_min >= rec.ph_max:
                raise ValidationError(_("pH Min harus lebih kecil dari pH Max."))
            if rec.visc_min >= rec.visc_max:
                raise ValidationError(
                    _("Visc Min harus lebih kecil dari Visc Max.")
                )

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

    def re_evaluate(self):
        """Buat keputusan baru dengan hasil uji yang sama.

        Riwayat lama tidak ditimpa: batch yang diuji ulang akan punya
        decision record sendiri supaya audit trail tetap utuh.
        """
        self.ensure_one()
        new_decision = self.copy({
            "state": "draft",
            "status": False,
            "recommendation": False,
            "ph_in_range": False,
            "viscosity_in_range": False,
            "api_response_raw": False,
            "user_id": self.env.user.id,
        })
        return {
            "type": "ir.actions.act_window",
            "res_model": "qc.kbr.decision",
            "res_id": new_decision.id,
            "view_mode": "form",
            "target": "current",
        }

    def _sync_spec_from_product(self):
        """Salin spesifikasi produk ke decision dan pastikan engine memakai spec itu."""
        for record in self:
            product = record.product_id
            if not product:
                continue
            record.write({
                "ph_min": product.qc_ph_min,
                "ph_max": product.qc_ph_max,
                "visc_min": product.qc_visc_min,
                "visc_max": product.qc_visc_max,
                "spec_version": product.qc_spec_version or "UNVERSIONED",
            })

    def submit_to_kbr(self):
        """Kirim data QC ke inference engine lalu catat hasilnya."""
        for record in self:
            if record.state in ("done", "failed"):
                raise UserError(
                    _("Decision already processed for %s") % record.name
                )

            record._sync_spec_from_product()

            try:
                result = call_qc_engine(
                    batch_id=record.batch_id or record.production_id.name,
                    ph_level=record.ph_level,
                    viscosity=record.viscosity,
                    spec={
                        "ph_min": record.ph_min,
                        "ph_max": record.ph_max,
                        "visc_min": record.visc_min,
                        "visc_max": record.visc_max,
                    },
                    api_key=self.env["ir.config_parameter"].sudo().get_param(
                        "qc_engine.api_key"
                    ),
                )
                vals = record._prepare_vals_from_engine(result)
                record.write(vals)
                record.production_id._update_from_kbr_decision(vals)
                _logger.info(
                    "KBR Decision: batch=%s → status=%s analyst=%s",
                    record.batch_id, vals["status"], record.user_id.login,
                )
            except UserError:
                record.write({"state": "failed"})
                raise
            except Exception as exc:  # pragma: no cover - defensive
                _logger.exception("KBR Decision gagal untuk %s", record.name)
                record.write({"state": "failed"})
                raise UserError(
                    _("Gagal memproses keputusan QC. Periksa log server.")
                ) from exc


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    kbr_decision_ids = fields.One2many(
        "qc.kbr.decision",
        "production_id",
        string="KBR Decisions",
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

    @api.depends("kbr_decision_ids.state", "kbr_decision_ids.status")
    def _compute_kbr_status(self):
        for rec in self:
            decisions = rec.kbr_decision_ids.filtered(lambda d: d.state == "done")
            rec.kbr_latest_status = decisions[:1].status or False

    def _update_from_kbr_decision(self, decision_vals: dict):
        """Catat hasil QC pada production order.

        Status MO tidak diubah langsung: `state` di Odoo managed oleh stock move
        dan harus lewat `button_mark_done` supaya move, valuasi, dan journal
        entry ikut terbentuk. Menulis `state` manual menghasilkan stok hantu.
        """
        status = decision_vals.get("status")

        if status == "approved":
            self.write({"qty_approved": self.qty_produced})
            self.message_post(
                body=_(
                    "<b>QC Approved</b><br/>%s unit siap dilepas. "
                    "Selesaikan production order lewat tombol 'Mark as Done'."
                ) % self.qty_produced,
                message_type="notification",
                subtype_xmlid="mail.mt_note",
            )
        elif status == "rework":
            self.message_post(
                body=_(
                    "<b>QC Rework Required</b><br/>"
                    "Recommendation: %s"
                ) % decision_vals.get("recommendation", ""),
                message_type="notification",
                subtype_xmlid="mail.mt_note",
            )
        elif status == "rejected":
            self.write({"qty_approved": 0.0})
            self.message_post(
                body=_(
                    "<b>QC Rejected</b><br/>"
                    "Recommendation: %s"
                ) % decision_vals.get("recommendation", ""),
                message_type="notification",
                subtype_xmlid="mail.mt_comment",
            )


class StockMove(models.Model):
    """Blokir pengiriman batch yang belum released QC."""

    _inherit = "stock.move"

    def _qc_blocking_decision(self):
        """Decision QC yang i'd/block list.

        Returns the blocking decision record (or empty recordset) for each move.
        """
        self.ensure_one()
        if self.state in ("done", "cancel"):
            return self.env["qc.kbr.decision"]
        if not self.product_id:
            return self.env["qc.kbr.decision"]
        if self.location_id.usage != "internal":
            # Only outgoing moves leave the warehouse.
            return self.env["qc.kbr.decision"]

        decision_model = self.env["qc.kbr.decision"]
        domain = [
            ("production_id.product_id", "=", self.product_id.id),
            ("state", "=", "done"),
            ("status", "in", ("rework", "rejected")),
        ]
        if self.lot_id:
            domain.append(("production_id.move_ids.lot_id", "=", self.lot_id.id))
        return decision_model.search(domain, limit=1)

    def _check_qc_release(self):
        for move in self:
            decision = move._qc_blocking_decision()
            if not decision:
                continue
            raise UserError(
                _("Produk %s belum lolos QC (status: %s pada batch %s). "
                  "Batch harus dirework atau di-reject sebelum bisa dikirim.")
                % (
                    move.product_id.display_name,
                    decision.status,
                    decision.batch_id,
                )
            )

    @api.model_create_multi
    def create(self, vals_list):
        moves = super().create(vals_list)
        moves._check_qc_release()
        return moves

    def write(self, vals):
        result = super().write(vals)
        if "product_id" in vals or "lot_id" in vals or "quantity" in vals:
            self._check_qc_release()
        return result
