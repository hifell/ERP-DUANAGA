from odoo import models, api
import logging

_logger = logging.getLogger(__name__)


class WebsiteLead(models.Model):
    _inherit = "crm.lead"

    @api.model
    def create_lead_from_website(self, data):
        """Create lead from website form submission"""
        vals = {
            "name": data.get("name", "Website Lead"),
            "contact_name": data.get("contact_name", ""),
            "email_from": data.get("email", ""),
            "phone": data.get("phone", ""),
            "description": data.get("message", ""),
            "type": "lead",
            "source_id": self.env.ref("crm_website.crm_source_website").id if False else False,
            "team_id": self.env.ref("sales_team.team_sales_department").id if False else False,
        }

        lead = self.create(vals)
        _logger.info(f"Lead created from website: {lead.id} - {lead.name}")

        # Trigger webhook to n8n for notification
        self._notify_n8n(lead)

        return lead.id

    def _notify_n8n(self, lead):
        """Send notification to n8n for WhatsApp alert"""
        import urllib.request
        import json

        try:
            webhook_url = "http://duanaga_n8n:5678/webhook/lead-notification"
            data = {
                "lead_id": lead.id,
                "name": lead.name,
                "contact_name": lead.contact_name,
                "email": lead.email_from,
                "phone": lead.phone,
                "message": lead.description,
            }

            req = urllib.request.Request(
                webhook_url,
                data=json.dumps(data).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=10):
                _logger.info(f"n8n notification sent for lead {lead.id}")
        except Exception as e:
            _logger.warning(f"Failed to notify n8n: {e}")
