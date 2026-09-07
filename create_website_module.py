#!/usr/bin/env python3
"""
Setup Custom Module untuk Lead Capture via Website
PT Dua Naga Kosmetindo
"""
import os

# Create custom module directory
module_dir = '/home/thufail/ERP_DUANAGA/addons/duanaga_website'
os.makedirs(f'{module_dir}/models', exist_ok=True)
os.makedirs(f'{module_dir}/controllers', exist_ok=True)
os.makedirs(f'{module_dir}/views', exist_ok=True)
os.makedirs(f'{module_dir}/security', exist_ok=True)

# __manifest__.py
manifest = '''{
    "name": "Dua Naga Website Integration",
    "version": "1.0",
    "category": "Sales",
    "summary": "Lead capture from website for PT Dua Naga Kosmetindo",
    "description": """
        Custom module untuk capture leads dari website duanaga.co.id
        - Lead capture endpoint
        - Auto-assign to sales team
        - Notifikasi ke WhatsApp via n8n
    """,
    "author": "PT Dua Naga Kosmetindo",
    "website": "https://duanaga.co.id",
    "license": "LGPL-3",
    "depends": ["crm", "sale"],
    "data": [
        "security/ir.model.access.csv",
        "views/lead_template.xml",
    ],
    "installable": True,
    "application": True,
}
'''

# models/__init__.py
models_init = '''from . import website_lead
'''

# models/website_lead.py
website_lead = '''from odoo import models, api
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
'''

# controllers/__init__.py
controllers_init = '''from . import website
'''

# controllers/website.py
website_controller = '''from odoo import http
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
'''

# views/lead_template.xml
lead_template = '''<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <template id="success">
        <t t-call="website.layout">
            <div class="container">
                <div class="alert alert-success">
                    <h2>Terima Kasih!</h2>
                    <p>Pertanyaan Anda telah kami terima. Tim kami akan segera menghubungi Anda.</p>
                    <a href="/" class="btn btn-primary">Kembali ke Beranda</a>
                </div>
            </div>
        </t>
    </template>

    <template id="error">
        <t t-call="website.layout">
            <div class="container">
                <div class="alert alert-danger">
                    <h2>Error</h2>
                    <p t-esc="message"/>
                    <a href="/" class="btn btn-primary">Kembali</a>
                </div>
            </div>
        </t>
    </template>
</odoo>
'''

# security/ir.model.access.csv
access_csv = '''id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_duanaga_website_user,duanaga.website.user,model_crm_lead,,1,1,1,1
'''

# Write files
with open(f'{module_dir}/__manifest__.py', 'w') as f:
    f.write(manifest)

with open(f'{module_dir}/models/__init__.py', 'w') as f:
    f.write(models_init)

with open(f'{module_dir}/models/website_lead.py', 'w') as f:
    f.write(website_lead)

with open(f'{module_dir}/controllers/__init__.py', 'w') as f:
    f.write(controllers_init)

with open(f'{module_dir}/controllers/website.py', 'w') as f:
    f.write(website_controller)

with open(f'{module_dir}/views/lead_template.xml', 'w') as f:
    f.write(lead_template)

os.makedirs(f'{module_dir}/security', exist_ok=True)
with open(f'{module_dir}/security/ir.model.access.csv', 'w') as f:
    f.write(access_csv)

print(f"✓ Custom module created: {module_dir}")
print(f"  - models/website_lead.py")
print(f"  - controllers/website.py")
print(f"  - views/lead_template.xml")
print(f"\nNext: Install module via Odoo > Apps > Update Apps List > Search 'dua naga'")
