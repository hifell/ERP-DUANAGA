from odoo import http
from odoo.http import request
import json
import logging

_logger = logging.getLogger(__name__)


class WebsiteLead(http.Controller):

    @http.route("/website/lead/submit", type="http", auth="public", website=True, csrf=False)
    def submit_lead(self, **post):
        """Handle lead submission from website form"""
        _logger.info(f"Lead submission: {post}")

        # Validate required fields
        if not post.get("name") or not post.get("email"):
            return request.render("duanaga_website.error", {
                "message": "Name and email are required"
            })

        # Create lead
        lead_id = request.env["crm.lead"].sudo().create_lead_from_website(post)

        return request.render("duanaga_website.success", {
            "lead_id": lead_id
        })


    @http.route("/api/lead", type="json", auth="public", csrf=False)
    def api_lead(self, **post):
        """JSON API for lead submission"""
        _logger.info(f"API Lead submission: {post}")

        if not post.get("name") or not post.get("email"):
            return {"success": False, "error": "Name and email required"}

        try:
            lead_id = request.env["crm.lead"].sudo().create_lead_from_website(post)
            return {"success": True, "lead_id": lead_id}
        except Exception as e:
            _logger.error(f"Failed to create lead: {e}")
            return {"success": False, "error": str(e)}
