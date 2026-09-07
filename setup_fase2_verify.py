#!/usr/bin/env python3
"""
setup_fase2_verify.py - Odoo 17 Module Installation Verification
Use this to verify module installation status
"""

import xmlrpc.client
import sys

# ============================================================================
# CONFIGURATION
# ============================================================================
ODOO_URL = "http://localhost:8069"
ODOO_DB = "duanaga_poc"
ODOO_USER = "thufail.alwafi123@gmail.com"
ODOO_PASSWORD = "Thufail123"

# ============================================================================
# MODULES TO VERIFY
# ============================================================================
MODULES = {
    'mrp': 'Manufacturing',
    'purchase': 'Purchase',
    'sale_management': 'Sale Management',
    'stock': 'Inventory',
    'product': 'Product',
    'account': 'Accounting',
    'sale': 'Sales',
    'resource': 'Resource',
    'digest': 'Digest',
}

# ============================================================================
# MAIN
# ============================================================================
def main():
    print("=" * 60)
    print("ODOO 17 MODULE VERIFICATION")
    print("=" * 60)

    # Connect
    common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
    models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")

    uid = common.authenticate(ODOO_DB, ODOO_USER, ODOO_PASSWORD, {})
    if not uid:
        print("[ERROR] Authentication failed")
        sys.exit(1)
    print(f"[OK] Authenticated as UID: {uid}\n")

    # Check modules
    print("Module Status:")
    print("-" * 40)

    installed = []
    pending = []
    missing = []

    for mod_name, mod_label in MODULES.items():
        ids = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'ir.module.module', 'search', [[['name', '=', mod_name]]])

        if not ids:
            print(f"  {mod_label:25} NOT FOUND")
            missing.append(mod_label)
            continue

        data = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'ir.module.module', 'read', [ids, ['state']])
        state = data[0]['state'] if data else 'unknown'

        if state == 'installed':
            print(f"  {mod_label:25} INSTALLED")
            installed.append(mod_label)
        else:
            print(f"  {mod_label:25} {state.upper()}")
            pending.append(mod_label)

    # Summary
    print("\n" + "=" * 60)
    print(f"Summary: {len(installed)}/{len(MODULES)} installed")
    print("=" * 60)

    if pending:
        print("\n[ACTION REQUIRED] Install pending modules manually:")
        print("  1. Open http://localhost:8069 in browser")
        print("  2. Go to: Apps > Search for module name")
        print("  3. Click Install button")
        print("\nRecommended installation order:")
        print("  1. Product (if not installed)")
        print("  2. Inventory (stock)")
        print("  3. Accounting (account)")
        print("  4. Purchase")
        print("  5. Digest + Sales")
        print("  6. Sale Management")
        print("  7. Manufacturing (mrp)")

    # Check traceability config
    print("\n" + "=" * 60)
    print("Traceability Configuration:")
    print("=" * 60)

    param_ids = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'ir.config_parameter', 'search',
                                  [[('key', '=', 'stock.group_production_lot')]])

    if param_ids:
        data = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'ir.config_parameter', 'read',
                                  [param_ids, ['value']])
        value = data[0]['value'] if data else '0'
        if value == '1':
            print("  group_stock_production_lot: ENABLED")
        else:
            print("  group_stock_production_lot: DISABLED")
    else:
        print("  group_stock_production_lot: NOT CONFIGURED")

    print("\n[NOTE] To enable via UI:")
    print("  Inventory > Configuration > Settings > Lots & Serial Numbers")


if __name__ == "__main__":
    main()
