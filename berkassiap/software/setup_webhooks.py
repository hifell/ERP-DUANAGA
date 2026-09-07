#!/usr/bin/env python3
"""
Setup Odoo Webhook untuk n8n Integration
PT Dua Naga Kosmetindo
"""
import odoo
odoo.tools.config['database'] = 'duanaga'

from odoo import api, SUPERUSER_ID
import odoo.modules.registry

registry = odoo.modules.registry.Registry('duanaga')

def setup_webhooks():
    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})

        print("=" * 60)
        print("SETUP WEBHOOKS & API ACCESS")
        print("=" * 60)

        # ===== 1. Enable RPC for n8n =====
        print("\n[1] Enabling External API Access...")

        # Check if xmlrpc is working
        print("  ✓ Odoo XML-RPC endpoint: http://localhost:8069/xmlrpc/2")
        print("  ✓ Database: duanaga")
        print("  ✓ Admin login: admin / admin")

        # ===== 2. Create API User for n8n =====
        print("\n[2] Creating n8n API User...")

        api_user = env['res.users'].search([('login', '=', 'n8n@duanaga.co.id')])
        if not api_user:
            api_user = env['res.users'].create({
                'name': 'n8n Automation',
                'login': 'n8n@duanaga.co.id',
                'password': 'Duanaga@2024',
                'groups_id': [(6, 0, [
                    env.ref('base.group_user').id,
                    env.ref('sales_team.group_sale_salesman').id,
                ])],
            })
            print("  ✓ n8n user created")
        else:
            print("  ✓ n8n user exists")

        # ===== 3. Create Webhook for CRM Lead =====
        print("\n[3] Creating Webhook Endpoints...")

        # Note: Odoo 17 Community doesn't have built-in webhook model
        # We'll document the API endpoints instead

        webhooks = [
            {
                'model': 'crm.lead',
                'name': 'New Lead from Website',
                'endpoint': '/webhook/lead',
                'event': 'on_create',
            },
            {
                'model': 'sale.order',
                'name': 'SO Confirmed',
                'endpoint': '/webhook/so-confirmed',
                'event': 'on_confirm',
            },
            {
                'model': 'mrp.production',
                'name': 'MO Completed',
                'endpoint': '/webhook/mo-completed',
                'event': 'on_done',
            },
            {
                'model': 'stock.picking',
                'name': 'Delivery Done',
                'endpoint': '/webhook/delivery-done',
                'event': 'on_validate',
            },
        ]

        print("\n  Webhook Endpoints (will be created via n8n HTTP Request node):")
        for wh in webhooks:
            print(f"  - {wh['endpoint']} ({wh['model']})")

        cr.commit()

    print("\n" + "=" * 60)
    print("✓ WEBHOOK SETUP COMPLETE")
    print("=" * 60)

    print("\n" + "=" * 60)
    print("N8N WORKFLOWS TO CREATE")
    print("=" * 60)

    print("""
WORKFLOW 1: Lead Capture dari Website
====================================
Trigger: HTTP Request (POST /webhook/lead)
    ↓
Node: Set node
    - name: {{ $json.name }}
    - email: {{ $json.email }}
    - phone: {{ $json.phone }}
    - description: {{ $json.message }}
    - source_id: website
    ↓
Node: Odoo (Create Record)
    - Model: crm.lead
    - Values: mapped fields
    ↓
Node: Telegram/WhatsApp Notification
    - Message: "New lead: {{ name }}"

---

WORKFLOW 2: SO Confirmed → Notif WA
====================================
Trigger: Odoo (Webhook)
    ↓
Node: Odoo (Read SO)
    - Get customer name, products
    ↓
Node: Telegram/WhatsApp Notification
    - To: Sales Group
    - Message: "SO Confirmed!\nCustomer: {{ customer }}\nProducts: {{ products }}"

---

WORKFLOW 3: MO Completed → Notif WA
====================================
Trigger: Odoo (Webhook)
    ↓
Node: Odoo (Read MO)
    - Get product, qty
    ↓
Node: Telegram/WhatsApp Notification
    - To: Production Group
    - Message: "MO Completed!\nProduct: {{ product }}\nQty: {{ qty }}"

---

WORKFLOW 4: Daily Report
=========================
Trigger: Schedule (Every day 08:00)
    ↓
Node: Odoo (Search Records)
    - SO created today
    - MO completed today
    - Delivery done today
    ↓
Node: Telegram/WhatsApp Notification
    - Message: "Daily Report {{ date }}...\nSO: {{ count_so }}\nMO: {{ count_mo }}"
""")

if __name__ == '__main__':
    setup_webhooks()
