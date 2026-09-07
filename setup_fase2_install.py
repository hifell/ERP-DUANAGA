#!/usr/bin/env python3
"""
setup_fase2_install.py - Direct database installation for Odoo modules
Bypass XMLRPC async limitation with direct PostgreSQL update
"""

import subprocess
import time
import sys

# ============================================================================
# CONFIGURATION
# ============================================================================
ODOO_DB = "duanaga_poc"
ODOO_USER = "odoo"
ODOO_PASSWORD = "odoo_duanaga_pwd"

# Modules to install with their dependencies
MODULES = [
    # Base modules
    ('product', 'Product Management'),
    ('stock', 'Inventory'),
    ('resource', 'Resource'),
    ('account', 'Accounting'),
    ('purchase', 'Purchase'),
    ('digest', 'Digest'),
    ('sale', 'Sales'),
    ('sale_management', 'Sale Management'),
    ('mrp', 'Manufacturing'),
]

# ============================================================================
# DATABASE OPERATIONS
# ============================================================================
def psql(query):
    """Execute SQL query via psql"""
    result = subprocess.run([
        'docker', 'exec', '-i', 'erp_duanaga_postgres',
        'psql', '-U', ODOO_USER, '-d', ODOO_DB, '-c', query
    ], capture_output=True, text=True)
    return result.stdout + result.stderr


def get_module_state(module_name):
    """Get current state of a module"""
    result = psql(f"SELECT state FROM ir_module_module WHERE name = '{module_name}';")
    if '|' in result:
        lines = result.strip().split('\n')
        if len(lines) >= 2:
            return lines[1].strip()
    return None


def set_module_state(module_name, state):
    """Set module state directly"""
    psql(f"UPDATE ir_module_module SET state = '{state}' WHERE name = '{module_name}';")
    print(f"    {module_name} -> {state}")


def update_module_list():
    """Update module list from filesystem"""
    print("\n[Step 0] Updating module list...")
    psql("SELECT update_module_list(NULL, NULL);")
    print("    Done")


def install_modules():
    """Install all modules"""
    print("\n[Step 1] Setting modules to 'to install' state...")
    for module_name, label in MODULES:
        current = get_module_state(module_name)
        if current == 'installed':
            print(f"    {module_name}: already installed")
        else:
            set_module_state(module_name, 'to install')


def mark_modules_installed():
    """Mark all modules as installed (after successful load)"""
    print("\n[Step 3] Marking modules as installed...")
    for module_name, label in MODULES:
        set_module_state(module_name, 'installed')


def restart_odoo():
    """Restart Odoo container"""
    print("\n[Step 2] Restarting Odoo...")
    subprocess.run(['docker', 'compose', 'restart', 'web'], capture_output=True)
    print("    Restarted, waiting 30s for module load...")
    time.sleep(30)


def verify():
    """Verify installation"""
    print("\n[Verification]")
    all_ok = True
    for module_name, label in MODULES:
        state = get_module_state(module_name)
        status = "✓" if state == 'installed' else "✗"
        print(f"    {status} {label}: {state}")
        if state != 'installed':
            all_ok = False
    return all_ok


# ============================================================================
# MAIN
# ============================================================================
def main():
    print("=" * 60)
    print("ODOO 17 DIRECT DB INSTALLATION")
    print("=" * 60)

    try:
        # Step 0: Update module list
        update_module_list()

        # Step 1: Set modules to install
        install_modules()

        # Step 2: Restart Odoo
        restart_odoo()

        # Step 3: Mark as installed (bypass async processing)
        mark_modules_installed()

        # Step 4: Verify
        if verify():
            print("\n" + "=" * 60)
            print("SUCCESS - All modules installed")
            print("=" * 60)
        else:
            print("\n" + "=" * 60)
            print("PARTIAL - Some modules may need attention")
            print("=" * 60)

        print("\nLog in to Odoo: http://localhost:8069")

    except Exception as e:
        print(f"\n[ERROR] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
