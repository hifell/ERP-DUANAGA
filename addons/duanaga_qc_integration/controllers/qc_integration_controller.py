# -*- coding: utf-8 -*-
"""
REST API Controller: QC Integration
Expose endpoint untuk sistem eksternal (lab equipment, IoT sensors)
Industri pattern: sistem lab kirim data → Odoo proses → KBR engine
"""

import logging
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class QcIntegrationController(http.Controller):
    """
    Webhook endpoint untuk QC data dari sistem eksternal.

    Usage:
      POST /qc_integration/api/v1/qc-check
      {
        "batch_id": "BATCH-2024-001",
        "ph_level": 6.0,
        "viscosity": 1.075,
        "production_id": 42,
        "api_key": "duanaga_lab_key_2024"
      }
    """
    _cp_path = "/qc_integration/api/v1"

    @http.route(
        "/qc_integration/api/v1/qc-check",
        type="json",
        auth="api_key",
        methods=["POST"],
        csrf=False,
    )
    def submit_qc_check(self):
        """
        Terima QC data dari lab system, buat decision, return result.
        Auth: API Key di header X-Api-Key
        """
        try:
            params = request.jsonrequest
        except Exception:
            return {
                "success": False,
                "error": "Invalid JSON payload",
            }

        batch_id = params.get("batch_id") or params.get("production_id")
        ph_level = params.get("ph_level")
        viscosity = params.get("viscosity")
        production_id = params.get("production_id")
        api_key = request.httprequest.headers.get("X-Api-Key")

        # Validate required fields
        if not all([batch_id, ph_level, viscosity]):
            return {
                "success": False,
                "error": "Missing required fields: batch_id, ph_level, viscosity",
            }

        # Validate API key (bisa di-configure di ir.config_parameter)
        valid_key = (
            request.env["ir.config_parameter"]
            .sudo()
            .get_param("qc_integration.api_key", "")
        )
        if api_key != valid_key:
            return {
                "success": False,
                "error": "Unauthorized",
            }, 401

        try:
            # Buat KBR decision record
            vals = {
                "ph_level": ph_level,
                "viscosity": viscosity,
                "state": "submitted",
            }
            if production_id:
                vals["production_id"] = production_id

            decision = (
                request.env["qc.kbr.decision"]
                .sudo()
                .create(vals)
            )
            decision.submit_to_kbr()

            return {
                "success": True,
                "decision_id": decision.name,
                "batch_id": decision.batch_id,
                "status": decision.status,
                "recommendation": decision.recommendation,
                "ph_in_range": decision.ph_in_range,
                "viscosity_in_range": decision.viscosity_in_range,
            }

        except Exception as e:
            _logger.error(f"KBR API error: {e}")
            return {
                "success": False,
                "error": str(e),
            }

    @http.route(
        "/qc_integration/api/v1/health",
        type="http",
        auth="public",
        methods=["GET"],
    )
    def health(self):
        """Health check endpoint."""
        return {"status": "ok", "service": "qc-integration-api"}
