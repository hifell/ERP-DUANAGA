{
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
