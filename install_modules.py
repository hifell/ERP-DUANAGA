#!/usr/bin/env python3
"""
Install Odoo modules via internal API
"""
import odoo
from odoo.tools import config

config.options['database'] = 'duanaga'
config.options['without_demo'] = True
config.options['stop_after_init'] = True

# Initialize
odoo.cli.main(['--config=/dev/null'])

# Import needed modules
import odoo.modules
import odoo.modules.registry

# Get registry
registry = odoo.modules.registry.Registry('duanaga')

modules_to_install = [
    'stock',
    'mrp',
    'purchase',
    'sale_management',
    'account',
    'hr',
    'quality',
    'contacts',
    'product',
]

print("Installing modules...")
with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})

    for module_name in modules_to_install:
        module = env['ir.module.module'].search([('name', '=', module_name)], limit=1)
        if module:
            if module.state == 'installed':
                print(f"  ✓ {module_name} already installed")
            elif module.state in ('uninstalled', 'to upgrade'):
                print(f"  → Installing {module_name}...")
                try:
                    module.button_install()
                    print(f"  ✓ {module_name} installed")
                except Exception as e:
                    print(f"  ✗ {module_name} failed: {e}")
            else:
                print(f"  - {module_name} state: {module.state}")
        else:
            print(f"  ✗ {module_name} not found")

print("\nCommitting...")
registry._commit()

print("\n✓ Done! Restart Odoo container to apply changes.")
