# -*- coding: utf-8 -*-
"""Lead capture dari website duanaga.co.id."""

import logging
import re

from odoo import api, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
MAX_FIELD_LENGTH = 255


class WebsiteLead(models.Model):
    _inherit = "crm.lead"

    @api.model
    def create_lead_from_website(self, data):
        """Buat lead dari form website.

        Dipanggil dari controller dengan `sudo()`, jadi user website tidak
        butuh hak akses Odoo. Validasi input tetap dilakukan di sini supaya
        data yang masuk ke CRM bersih.
        """
        name = (data.get("name") or "").strip()[:MAX_FIELD_LENGTH]
        email = (data.get("email") or "").strip()[:MAX_FIELD_LENGTH]
        if not name:
            raise ValidationError("Name is required.")
        if not email or not EMAIL_RE.match(email):
            raise ValidationError("A valid email address is required.")

        vals = {
            "name": name,
            "contact_name": (data.get("contact_name") or name)[:MAX_FIELD_LENGTH],
            "email_from": email,
            "phone": (data.get("phone") or "")[:MAX_FIELD_LENGTH],
            "description": (data.get("message") or "")[:2000],
            "type": "lead",
        }

        source = self.env.ref(
            "crm_website.crm_source_website", raise_if_not_found=False
        )
        if source:
            vals["source_id"] = source.id
        team = self.env.ref(
            "sales_team.team_sales_department", raise_if_not_found=False
        )
        if team:
            vals["team_id"] = team.id

        lead = self.create(vals)
        _logger.info("Lead created from website: %s", lead.id)
        return lead.id
