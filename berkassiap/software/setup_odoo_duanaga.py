#!/usr/bin/env python3
"""
Auto Setup Odoo untuk PT Dua Naga Kosmetindo
Maklon kosmetik - Skincare, Haircare, Body Care, Cosmetics
"""

import xmlrpc.client
import sys
import time

# Config
URL = "http://localhost:8069"
ADMIN_PASS = "admin_duanaga_secure_2024"
DB_NAME = "duanaga"
ADMIN_EMAIL = "marketing@duanaga.co.id"
ADMIN_PASSWORD = "Duanaga@2024"

def get_common():
    return xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/common")

def get_models():
    return xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/object")

def check_db_exists():
    common = get_common()
    db_service = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/db")
    dbs = db_service.list()
    return DB_NAME in dbs

def create_database():
    print("\n⚠️  Odoo 17 tidak support create database via XML-RPC.")
    print("   Buka browser: http://localhost:8069")
    print("   1. Klik 'Create Database'")
    print(f"   2. Master Password: {ADMIN_PASS}")
    print(f"   3. Database Name: {DB_NAME}")
    print(f"   4. Email: {ADMIN_EMAIL}")
    print(f"   5. Password: {ADMIN_PASSWORD}")
    print("   6. Language: Indonesian")
    print("   7. Country: Indonesia")
    print("\n   Setelah selesai, jalankan ulang script ini.")
    sys.exit(1)

def get_uid():
    common = get_common()
    # Try different passwords
    passwords = [ADMIN_PASSWORD, "admin", "admin_duanaga", "duanaga", "password", "Duanaga2024", "Duanaga@2024"]
    for pwd in passwords:
        uid = common.authenticate(DB_NAME, "admin", pwd, {})
        if uid:
            print(f"  → Login berhasil dengan password: {pwd}")
            return uid
    return False

def install_modules(uid):
    models = get_models()
    print("[2/7] Cek modules...")
    print("  ✓ Modules biasanya sudah terinstall saat create DB")
    print("  ✓ Skip install modules via XMLRPC (harus via UI dengan admin)")

def setup_company(uid):
    models = get_models()
    print("[3/7] Setup company info...")

    # Get company IDs
    company_ids = models.execute_kw(
        DB_NAME, uid, ADMIN_PASSWORD,
        'res.company', 'search', [[]]
    )

    # Update company
    models.execute_kw(
        DB_NAME, uid, ADMIN_PASSWORD,
        'res.company', 'write',
        [company_ids[0] if company_ids else 1],
        [{
            'name': 'PT. Dua Naga Kosmetindo',
            'street': 'Dk. Gambiran, Ds. Krajan',
            'street2': 'Kec. Gatak, Kab. Sukoharjo',
            'city': 'Sukoharjo',
            'state_id': 1379,  # Jawa Tengah
            'zip': '57557',
            'country_id': 100,  # Indonesia
            'phone': '+62 811-2127-464',
            'email': 'marketing@duanaga.co.id',
            'website': 'https://duanaga.co.id',
            'vat': '01.234.567.8-901.000',
        }]
    )
    print("  ✓ Company info diupdate")

def create_product_categories(uid):
    models = get_models()
    print("[4/7] Membuat product categories...")

    categories = [
        ("Kosmetik", None),
        ("Face Care", "Kosmetik"),
        ("Body Care", "Kosmetik"),
        ("Hair Care", "Kosmetik"),
        ("Sunscreen", "Kosmetik"),
        ("Lip Care", "Kosmetik"),
        ("Eye Care", "Kosmetik"),
        ("Baby/Kids Care", "Kosmetik"),
        ("Men Care", "Kosmetik"),
        ("Face Masks", "Kosmetik"),
        ("Bahan Baku", None),
        ("Packaging", None),
    ]

    cat_map = {}
    for name, parent in categories:
        parent_id = cat_map.get(parent) if parent else False
        ids = models.execute_kw(
            DB_NAME, uid, ADMIN_PASSWORD,
            'product.category', 'search',
            [[['name', '=', name]]]
        )
        if not ids:
            ids = models.execute_kw(
                DB_NAME, uid, ADMIN_PASSWORD,
                'product.category', 'create',
                [{'name': name, 'parent_id': parent_id}]
            )
            cat_map[name] = ids
            print(f"  → {name} dibuat")
        else:
            cat_map[name] = ids[0]
            print(f"  ✓ {name} (ada)")

    return cat_map

def create_products(uid, categories):
    models = get_models()
    print("[5/7] Membuat sample products...")

    products = [
        # Finish Goods
        {"name": "Face Serum Vitamin C", "categ_id": categories["Face Care"], "type": "product", "list_price": 85000, "default_code": "FC-001"},
        {"name": "Body Lotion Whitening", "categ_id": categories["Body Care"], "type": "product", "list_price": 65000, "default_code": "BC-001"},
        {"name": "Hair Shampoo Anti Dandruff", "categ_id": categories["Hair Care"], "type": "product", "list_price": 45000, "default_code": "HC-001"},
        {"name": "Sunscreen SPF 50", "categ_id": categories["Sunscreen"], "type": "product", "list_price": 75000, "default_code": "SS-001"},
        {"name": "Lip Balm Moisturizing", "categ_id": categories["Lip Care"], "type": "product", "list_price": 35000, "default_code": "LC-001"},
        {"name": "Eye Cream Anti Aging", "categ_id": categories["Eye Care"], "type": "product", "list_price": 120000, "default_code": "EC-001"},
        {"name": "Baby Lotion Gentle", "categ_id": categories["Baby/Kids Care"], "type": "product", "list_price": 55000, "default_code": "BK-001"},
        {"name": "Men Face Wash", "categ_id": categories["Men Care"], "type": "product", "list_price": 48000, "default_code": "MC-001"},
        {"name": "Sheet Mask Hydrating", "categ_id": categories["Face Masks"], "type": "product", "list_price": 25000, "default_code": "FM-001"},
        # Raw Materials
        {"name": "Vitamin C Powder", "categ_id": categories["Bahan Baku"], "type": "consu", "list_price": 500000, "default_code": "BB-001"},
        {"name": "Shea Butter", "categ_id": categories["Bahan Baku"], "type": "consu", "list_price": 350000, "default_code": "BB-002"},
        {"name": "Glycerin USP", "categ_id": categories["Bahan Baku"], "type": "consu", "list_price": 180000, "default_code": "BB-003"},
        # Packaging
        {"name": "Botol Serum 30ml", "categ_id": categories["Packaging"], "type": "consu", "list_price": 3500, "default_code": "PK-001"},
        {"name": "Pump Dispenser", "categ_id": categories["Packaging"], "type": "consu", "list_price": 2000, "default_code": "PK-002"},
        {"name": "Box Packaging", "categ_id": categories["Packaging"], "type": "consu", "list_price": 2500, "default_code": "PK-003"},
    ]

    for p in products:
        ids = models.execute_kw(
            DB_NAME, uid, ADMIN_PASSWORD,
            'product.template', 'search',
            [[['default_code', '=', p['default_code']]]]
        )
        if not ids:
            models.execute_kw(
                DB_NAME, uid, ADMIN_PASSWORD,
                'product.template', 'create',
                [p]
            )
            print(f"  → {p['name']} dibuat")
        else:
            print(f"  ✓ {p['name']} (ada)")

    print("  ✓ Products dibuat")

def create_partners(uid):
    models = get_models()
    print("[6/7] Membuat sample partners (klien)...")

    partners = [
        {"name": "Beauty Glow Indonesia", "customer_rank": 1, "phone": "+62 21 1234 5678", "email": "order@beautyglow.id", "street": "Jakarta"},
        {"name": "SkinLab Clinic", "customer_rank": 1, "phone": "+62 21 9876 5432", "email": "purchasing@skinlab.co.id", "street": "Jakarta"},
        {"name": "Spa Serenity Bali", "customer_rank": 1, "phone": "+62 361 123 456", "email": "order@spaserenity.bali", "street": "Bali"},
        {"name": "Hotel Bintang Surabaya", "customer_rank": 1, "phone": "+62 31 456 789", "email": "procurement@hotelbintang.surabaya", "street": "Surabaya"},
        {"name": "Supplier Bahan Kimia - CV Chemindo", "supplier_rank": 1, "phone": "+62 21 555 1234", "email": "sales@chemindo.co.id", "street": "Tangerang"},
        {"name": "Supplier Packaging - PT Packpro", "supplier_rank": 1, "phone": "+62 21 777 8888", "email": "sales@packpro.id", "street": "Bekasi"},
    ]

    for partner in partners:
        ids = models.execute_kw(
            DB_NAME, uid, ADMIN_PASSWORD,
            'res.partner', 'search',
            [[['name', '=', partner['name']]]]
        )
        if not ids:
            models.execute_kw(
                DB_NAME, uid, ADMIN_PASSWORD,
                'res.partner', 'create',
                [partner]
            )
            print(f"  → {partner['name']} dibuat")
        else:
            print(f"  ✓ {partner['name']} (ada)")

    print("  ✓ Partners dibuat")

def create_users(uid):
    models = get_models()
    print("[7/7] Membuat user accounts...")

    users = [
        {"name": "Marketing Team", "login": "marketing@duanaga.co.id", "groups_id": [(6, 0, [21, 74])]},  # sales
        {"name": "Produksi Manager", "login": "produksi@duanaga.co.id", "groups_id": [(6, 0, [21, 47])]},  # mrp user
        {"name": "QC Supervisor", "login": "qc@duanaga.co.id", "groups_id": [(6, 0, [21, 92])]},  # quality
        {"name": "Gudang Staff", "login": "gudang@duanaga.co.id", "groups_id": [(6, 0, [21, 86])]},  # stock
        {"name": "Purchasing", "login": "purchasing@duanaga.co.id", "groups_id": [(6, 0, [21, 69])]},  # purchase
    ]

    for user in users:
        ids = models.execute_kw(
            DB_NAME, uid, ADMIN_PASSWORD,
            'res.users', 'search',
            [[['login', '=', user['login']]]]
        )
        if not ids:
            models.execute_kw(
                DB_NAME, uid, ADMIN_PASSWORD,
                'res.users', 'create',
                [{
                    'name': user['name'],
                    'login': user['login'],
                    'password': 'Duanaga@2024',
                    'groups_id': user['groups_id'],
                }]
            )
            print(f"  → {user['name']} ({user['login']}) dibuat")
        else:
            print(f"  ✓ {user['name']} (ada)")

    print("  ✓ Users dibuat")

def main():
    print("=" * 50)
    print("SETUP ODOO - PT DUA NAGA KOSMETINDO")
    print("=" * 50)

    # Check database
    if not check_db_exists():
        print("\n⚠️  Database 'duanaga' belum ada!")
        print("   Buka browser: http://localhost:8069")
        print("   Buat database baru, lalu jalankan ulang script ini.")
        sys.exit(1)

    print("  ✓ Database 'duanaga' ditemukan!")

    # Get UID
    uid = get_uid()
    if not uid:
        print("ERROR: Gagal login! Database mungkin belum selesai dibuat.")
        print("Tunggu 30 detik, lalu jalankan ulang script ini.")
        sys.exit(1)

    print(f"\nLogin berhasil! UID: {uid}")

    # Setup steps
    install_modules(uid)
    setup_company(uid)
    categories = create_product_categories(uid)
    create_products(uid, categories)
    create_partners(uid)
    create_users(uid)

    print("\n" + "=" * 50)
    print("✓ SETUP SELESAI!")
    print("=" * 50)
    print(f"\nBuka browser: http://localhost:8069")
    print(f"Login: admin")
    print(f"Password: Duanaga@2024")
    print(f"Database: {DB_NAME}")

if __name__ == "__main__":
    main()
