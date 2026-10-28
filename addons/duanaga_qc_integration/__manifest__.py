{
    "name": "Duanaga QC KBR Integration",
    "version": "17.0.1.0.0",
    "description": "Integrasi Knowledge-Based Reasoning Engine untuk Quality Control kosmetik",
    "author": "Duanaga ERP Team",
    "license": "LGPL-3",
    "depends": ["mrp", "stock", "product", "mail"],
    "data": [
        "security/qc_security.xml",
        "security/ir.model.access.csv",
        "data/quality_data.xml",
        "data/qc_menu.xml",
        "views/qc_integration_views.xml",
        "views/mrp_production_views.xml",
        "views/qc_kbr_views.xml",
    ],
    "application": True,
    "installable": True,
}
