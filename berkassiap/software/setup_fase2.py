#!/usr/bin/env python3
"""
setup_fase2.py - Odoo 17 Manufacturing Phase 2 Automation
"""

import xmlrpc.client
import sys
import subprocess
import time

# ============================================================================
# CONFIGURATION
# ============================================================================
ODOO_URL = "http://localhost:8069"
ODOO_DB = "duanaga_poc"
ODOO_USER = "thufail.alwafi123@gmail.com"
ODOO_PASSWORD = "Thufail123"

# ============================================================================
# XMLRPC CLIENTS
# ============================================================================
common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================
def authenticate():
    """Authenticate to Odoo and return uid"""
    print("[1/3] Authenticating to Odoo...")
    uid = common.authenticate(ODOO_DB, ODOO_USER, ODOO_PASSWORD, {})
    if uid:
        print(f"    [OK] Authenticated successfully. UID: {uid}")
        return uid
    print("    [FAIL] Authentication failed")
    return None


def execute_kw(model, method, args, kwargs=None):
    if kwargs is None:
        kwargs = {}
    return models.execute_kw(ODOO_DB, UID, ODOO_PASSWORD, model, method, args, kwargs)


def search(model, domain):
    return execute_kw(model, 'search', [domain])


def search_read(model, domain, fields=None):
    if fields:
        return execute_kw(model, 'search_read', [domain], {'fields': fields})
    return execute_kw(model, 'search_read', [domain])


def write(model, ids, values):
    return execute_kw(model, 'write', [ids, values])


def call(model, method, args):
    return execute_kw(model, method, args)


def get_module_state(module_name):
    ids = search('ir.module.module', [('name', '=', module_name)])
    if not ids:
        return None
    data = search_read('ir.module.module', [('id', '=', ids[0])], ['state'])
    return data[0]['state'] if data else None


def trigger_install(module_name):
    """Trigger module installation without waiting"""
    ids = search('ir.module.module', [('name', '=', module_name)])
    if not ids:
        print(f"        [SKIP] Module '{module_name}' not found")
        return False

    state = get_module_state(module_name)
    if state == 'installed':
        print(f"        [OK] {module_name}: already installed")
        return True

    if state in ['uninstallable', 'broken']:
        print(f"        [SKIP] {module_name}: unusable state ({state})")
        return False

    # Trigger installation
    write('ir.module.module', ids, {'state': 'to install'})
    call('ir.module.module', 'button_immediate_install', [ids])
    print(f"        [TRIGGERED] {module_name} installation queued")
    return True


# ============================================================================
# MODULE 2: INSTALL CORE MODULES
# ============================================================================
def install_modules():
    """Install MRP, Purchase, and Sale Management modules"""
    print("\n[2/3] Installing Core Modules...")

    # All modules to install in dependency order
    modules = [
        'product',           # Base product management
        'stock',             # Inventory (needs product)
        'resource',          # Resource management
        'account',           # Accounting (needed for purchase)
        'purchase',          # Purchase (needs account)
        'digest',            # Dashboard digest
        'sale',              # Sales (needs digest)
        'sale_management',   # Sales management (needs sale)
        'mrp',               # Manufacturing (needs stock, product, resource)
    ]

    # Step 1: Trigger all installations
    print("\n    Phase 1: Triggering installations...")
    for module in modules:
        state = get_module_state(module)
        print(f"    {module}: {state}")
        trigger_install(module)

    # Step 2: Restart Odoo to process the queue
    print("\n    Phase 2: Restarting Odoo to process installations...")
    print("    (This triggers the module installation cron job)")
    subprocess.run(['docker', 'compose', 'restart', 'web'], capture_output=True)
    print("    Odoo restarting... (30 seconds)")
    time.sleep(30)

    # Step 3: Check results
    print("\n    Phase 3: Verification...")
    installed_count = 0
    for module in modules:
        state = get_module_state(module)
        if state == 'installed':
            print(f"    [OK] {module}: installed")
            installed_count += 1
        elif state == 'to install':
            print(f"    [PENDING] {module}: still installing")
        else:
            print(f"    [INFO] {module}: {state}")

    print(f"\n    Modules installed: {installed_count}/{len(modules)}")

    if installed_count < len(modules):
        print("\n    Some modules pending. Run script again after 60 seconds.")
        print("    Or install manually via Odoo web UI: Apps > Update Apps List")


# ============================================================================
# MODULE 3: CONFIGURE BPOM TRACEABILITY
# ============================================================================
def configure_bpom_traceability():
    """Enable Lots & Serial Numbers for BPOM compliance"""
    print("\n[3/3] Configuring BPOM Traceability...")

    # Check if stock module is available
    stock_state = get_module_state('stock')
    if stock_state != 'installed':
        print(f"    [WARN] Stock module not installed ({stock_state})")

    try:
        # Method: Set via ir.config_parameter
        print("    Setting lot tracking configuration...")

        # Main setting
        param_ids = search('ir.config_parameter', [('key', '=', 'stock.group_production_lot')])
        if param_ids:
            write('ir.config_parameter', param_ids, {'value': '1'})
            print("    [OK] stock.group_production_lot = 1")
        else:
            call('ir.config_parameter', 'create', [[{
                'key': 'stock.group_production_lot',
                'value': '1',
            }]])
            print("    [OK] Created stock.group_production_lot")

        # Additional setting for product lots
        lot_ids = search('ir.config_parameter', [('key', '=', 'stock.group_stock_lot')])
        if lot_ids:
            write('ir.config_parameter', lot_ids, {'value': '1'})
            print("    [OK] stock.group_stock_lot = 1")
        else:
            call('ir.config_parameter', 'create', [[{
                'key': 'stock.group_stock_lot',
                'value': '1',
            }]])
            print("    [OK] Created stock.group_stock_lot")

        print("    [OK] Traceability configuration complete")

    except Exception as e:
        print(f"    [ERROR] {e}")


# ============================================================================
# MAIN
# ============================================================================
def main():
    print("=" * 60)
    print("ODOO 17 MANUFACTURING PHASE 2 SETUP")
    print("=" * 60)

    global UID
    UID = authenticate()
    if not UID:
        sys.exit(1)

    install_modules()
    configure_bpom_traceability()

    print("\n" + "=" * 60)
    print("SETUP COMPLETE")
    print("=" * 60)
    print("Next steps:")
    print("  1. Wait 60 seconds for installations to complete")
    print("  2. Run this script again to verify")
    print("  3. Log in to Odoo web: http://localhost:8069")
    print("  4. Verify modules in: Apps > Search (Manufacturing, Purchase, etc)")
    print("  5. Enable tracking: Inventory > Configuration > Settings")
    print("=" * 60)


if __name__ == "__main__":
    main()
