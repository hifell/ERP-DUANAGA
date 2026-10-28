# -*- coding: utf-8 -*-
"""
REST API Controller: QC Integration
Endpoint untuk sistem eksternal (lab equipment, IoT sensors) mengirim
hasil pengujian QC ke Odoo.

  POST /qc_integration/api/v1/qc-check
  Header: X-Api-Key: <key dari ir.config_parameter qc_integration.api_key>
  Body:  {"batch_id": "MO00001", "ph_level": 6.0, "viscosity": 1.075,
          "production_id": 42}
"""

import hmac
import logging

from odoo import http
from odoo.http import request

from werkzeug.exceptions import BadRequest, ServiceUnavailable, Unauthorized

_logger = logging.getLogger(__name__)


class QcIntegrationController(http.Controller):
    """Webhook endpoint untuk QC data dari sistem eksternal."""

    _cp_path = "/qc_integration/api/v1"

    def _configured_api_key(self):
        return (
            request.env["ir.config_parameter"]
            .sudo()
            .get_param("qc_integration.api_key", "")
            .strip()
        )

    def _authorise(self):
        """Return True kalau request membawa API key yang benar."""
        configured = self._configured_api_key()
        if not configured:
            # Fail closed: tanpa key yang dikonfigurasi, endpoint tidak boleh dipakai.
            raise ServiceUnavailable(
                "QC integration API key is not configured on the server."
            )
        provided = request.httprequest.headers.get("X-Api-Key", "") or ""
        if not hmac.compare_digest(provided.encode(), configured.encode()):
            raise Unauthorized("Invalid or missing X-Api-Key header.")

    def _service_user(self):
        """User Odoo yang dicatat sebagai analyst untuk request mesin."""
        login = (
            request.env["ir.config_parameter"]
            .sudo()
            .get_param("qc_integration.service_user_login", "")
            .strip()
        )
        if not login:
            return request.env["res.users"].browse()
        return request.env["res.users"].search([("login", "=", login)], limit=1)

    @http.route(
        "/qc_integration/api/v1/qc-check",
        type="http",
        auth="public",
        methods=["POST"],
        csrf=False,
        save_session=False,
    )
    def submit_qc_check(self):
        """Terima hasil uji lab, buat keputusan QC, return hasilnya."""
        self._authorise()

        try:
            params = request.jsonrequest
        except Exception as exc:
            raise BadRequest("Invalid JSON payload.") from exc

        if not isinstance(params, dict):
            raise BadRequest("JSON payload must be an object.")

        batch_id = params.get("batch_id")
        production_id = params.get("production_id")
        ph_level = params.get("ph_level")
        viscosity = params.get("viscosity")

        if not (batch_id or production_id):
            raise BadRequest("Missing required field: batch_id or production_id.")
        if ph_level is None or viscosity is None:
            raise BadRequest("Missing required fields: ph_level, viscosity.")

        try:
            ph_level = float(ph_level)
            viscosity = float(viscosity)
        except (TypeError, ValueError) as exc:
            raise BadRequest("ph_level and viscosity must be numeric.") from exc

        if not 0.0 <= ph_level <= 14.0:
            raise BadRequest("ph_level must be between 0 and 14.")
        if viscosity < 0.0:
            raise BadRequest("viscosity must not be negative.")

        decision_model = request.env["qc.kbr.decision"].sudo()
        if production_id:
            production = request.env["mrp.production"].browse(production_id).exists()
            if not production:
                raise BadRequest(f"Unknown production_id: {production_id}")
        else:
            production = decision_model.search(
                [("batch_id", "=", batch_id)], limit=1
            ).production_id
            if not production:
                raise BadRequest(f"No production order found for batch {batch_id}.")

        vals = {
            "production_id": production.id,
            "ph_level": ph_level,
            "viscosity": viscosity,
            "state": "submitted",
        }
        service_user = self._service_user()
        if service_user:
            vals["user_id"] = service_user.id

        decision = decision_model.create(vals)

        try:
            decision.submit_to_kbr()
        except Exception:
            _logger.exception("KBR submission failed for batch %s", batch_id)
            raise ServiceUnavailable("QC engine call failed; decision recorded as failed.")

        return {
            "success": True,
            "decision_id": decision.name,
            "batch_id": decision.batch_id,
            "status": decision.status,
            "recommendation": decision.recommendation,
            "ph_in_range": decision.ph_in_range,
            "viscosity_in_range": decision.viscosity_in_range,
        }

    @http.route(
        "/qc_integration/api/v1/health",
        type="http",
        auth="public",
        methods=["GET"],
        save_session=False,
    )
    def health(self):
        """Health check endpoint."""
        return request.make_json_response({
            "status": "ok",
            "service": "qc-integration-api",
        })
