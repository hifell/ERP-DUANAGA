# -*- coding: utf-8 -*-
"""Endpoint publik untuk menerima lead dari website."""

import logging

from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request

_logger = logging.getLogger(__name__)

SUCCESS_HTML = """<!doctype html>
<html lang="id"><head><meta charset="utf-8"><title>Terima Kasih</title></head>
<body style="font-family:sans-serif;padding:3rem;text-align:center">
<h1>Terima Kasih!</h1>
<p>Pertanyaan Anda telah kami terima. Tim kami akan segera menghubungi Anda.</p>
<a href="/">Kembali ke Beranda</a>
</body></html>"""

ERROR_HTML = """<!doctype html>
<html lang="id"><head><meta charset="utf-8"><title>Error</title></head>
<body style="font-family:sans-serif;padding:3rem;text-align:center">
<h1>Terjadi kesalahan</h1>
<p>{message}</p>
<a href="/">Kembali</a>
</body></html>"""


class WebsiteLead(http.Controller):

    @http.route(
        "/website/lead/submit",
        type="http",
        auth="public",
        methods=["POST"],
        csrf=False,
        save_session=False,
    )
    def submit_lead(self, **post):
        """Handle lead submission dari form website."""
        try:
            lead_id = request.env["crm.lead"].sudo().create_lead_from_website(post)
        except ValidationError as exc:
            return request.make_response(
                ERROR_HTML.format(message=str(exc)), status=400,
                headers=[("Content-Type", "text/html; charset=utf-8")],
            )
        except Exception:
            _logger.exception("Gagal membuat lead dari website")
            return request.make_response(
                ERROR_HTML.format(
                    message="Permintaan tidak dapat diproses. Coba lagi nanti."
                ),
                status=500,
                headers=[("Content-Type", "text/html; charset=utf-8")],
            )
        return request.make_response(
            SUCCESS_HTML, headers=[("Content-Type", "text/html; charset=utf-8")]
        )

    @http.route(
        "/api/lead",
        type="json",
        auth="public",
        methods=["POST"],
        csrf=False,
        save_session=False,
    )
    def api_lead(self, **post):
        """JSON API untuk lead submission."""
        try:
            lead_id = request.env["crm.lead"].sudo().create_lead_from_website(post)
        except ValidationError as exc:
            return {"success": False, "error": str(exc)}
        except Exception:
            _logger.exception("Gagal membuat lead dari API website")
            return {
                "success": False,
                "error": "Permintaan tidak dapat diproses. Coba lagi nanti.",
            }
        return {"success": True, "lead_id": lead_id}
