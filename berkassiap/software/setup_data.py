#!/usr/bin/env python3
"""
Setup data untuk PT Dua Naga Kosmetindo
"""
import odoo

odoo.tools.config['database'] = 'duanaga'
odoo.tools.config['without_demo'] = True

import odoo.modules.registry
from odoo import api, SUPERUSER_ID

registry = odoo.modules.registry.Registry('duanaga')

def setup_all():
    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})

        print("[1/6] Setup Company...")
        # Update company
        company = env.company
        company.write({
            'name': 'PT. Dua Naga Kosmetindo',
            'street': 'Dk. Gambiran, Ds. Krajan',
            'street2': 'Kec. Gatak, Kab. Sukoharjo',
            'city': 'Sukoharjo',
            'state_id': 622,  # Jawa Tengah
            'zip': '57557',
            'country_id': 100,  # Indonesia
            'phone': '+62 811-2127-464',
            'email': 'marketing@duanaga.co.id',
            'website': 'https://duanaga.co.id',
        })
        print("  ✓ Company updated")

        print("[2/6] Create Product Categories...")
        categories = [
            'Kosmetik',
            'Face Care',
            'Body Care',
            'Hair Care',
            'Sunscreen',
            'Lip Care',
            'Eye Care',
            'Baby/Kids Care',
            'Men Care',
            'Face Masks',
            'Bahan Baku',
            'Packaging',
        ]
        cat_map = {}
        for name in categories:
            cat = env['product.category'].search([('name', '=', name)])
            if not cat:
                cat = env['product.category'].create({'name': name})
                print(f"  → {name} created")
            else:
                print(f"  ✓ {name} exists")
            cat_map[name] = cat.id
        print("  ✓ Categories done")

        print("[3/6] Create Products...")
        products = [
            # Finish Goods
            {'name': 'Face Serum Vitamin C', 'categ_id': cat_map['Face Care'], 'type': 'product', 'list_price': 85000, 'default_code': 'FC-001'},
            {'name': 'Body Lotion Whitening', 'categ_id': cat_map['Body Care'], 'type': 'product', 'list_price': 65000, 'default_code': 'BC-001'},
            {'name': 'Hair Shampoo Anti Dandruff', 'categ_id': cat_map['Hair Care'], 'type': 'product', 'list_price': 45000, 'default_code': 'HC-001'},
            {'name': 'Sunscreen SPF 50', 'categ_id': cat_map['Sunscreen'], 'type': 'product', 'list_price': 75000, 'default_code': 'SS-001'},
            {'name': 'Lip Balm Moisturizing', 'categ_id': cat_map['Lip Care'], 'type': 'product', 'list_price': 35000, 'default_code': 'LC-001'},
            {'name': 'Eye Cream Anti Aging', 'categ_id': cat_map['Eye Care'], 'type': 'product', 'list_price': 120000, 'default_code': 'EC-001'},
            {'name': 'Baby Lotion Gentle', 'categ_id': cat_map['Baby/Kids Care'], 'type': 'product', 'list_price': 55000, 'default_code': 'BK-001'},
            {'name': 'Men Face Wash', 'categ_id': cat_map['Men Care'], 'type': 'product', 'list_price': 48000, 'default_code': 'MC-001'},
            {'name': 'Sheet Mask Hydrating', 'categ_id': cat_map['Face Masks'], 'type': 'product', 'list_price': 25000, 'default_code': 'FM-001'},
            # Raw Materials
            {'name': 'Vitamin C Powder', 'categ_id': cat_map['Bahan Baku'], 'type': 'consu', 'list_price': 500000, 'default_code': 'BB-001'},
            {'name': 'Shea Butter', 'categ_id': cat_map['Bahan Baku'], 'type': 'consu', 'list_price': 350000, 'default_code': 'BB-002'},
            {'name': 'Glycerin USP', 'categ_id': cat_map['Bahan Baku'], 'type': 'consu', 'list_price': 180000, 'default_code': 'BB-003'},
            # Packaging
            {'name': 'Botol Serum 30ml', 'categ_id': cat_map['Packaging'], 'type': 'consu', 'list_price': 3500, 'default_code': 'PK-001'},
            {'name': 'Pump Dispenser', 'categ_id': cat_map['Packaging'], 'type': 'consu', 'list_price': 2000, 'default_code': 'PK-002'},
            {'name': 'Box Packaging', 'categ_id': cat_map['Packaging'], 'type': 'consu', 'list_price': 2500, 'default_code': 'PK-003'},
        ]
        for p in products:
            prod = env['product.template'].search([('default_code', '=', p['default_code'])])
            if not prod:
                prod = env['product.template'].create(p)
                print(f"  → {p['name']} created")
            else:
                print(f"  ✓ {p['name']} exists")
        print("  ✓ Products done")

        print("[4/6] Create Partners (Customers & Suppliers)...")
        partners = [
            # Customers
            {'name': 'Beauty Glow Indonesia', 'customer_rank': 1, 'phone': '+62 21 1234 5678', 'email': 'order@beautyglow.id', 'street': 'Jakarta'},
            {'name': 'SkinLab Clinic', 'customer_rank': 1, 'phone': '+62 21 9876 5432', 'email': 'purchasing@skinlab.co.id', 'street': 'Jakarta'},
            {'name': 'Spa Serenity Bali', 'customer_rank': 1, 'phone': '+62 361 123 456', 'email': 'order@spaserenity.bali', 'street': 'Bali'},
            {'name': 'Hotel Bintang Surabaya', 'customer_rank': 1, 'phone': '+62 31 456 789', 'email': 'procurement@hotelbintang.surabaya', 'street': 'Surabaya'},
            # Suppliers
            {'name': 'CV Chemindo (Bahan Kimia)', 'supplier_rank': 1, 'phone': '+62 21 555 1234', 'email': 'sales@chemindo.co.id', 'street': 'Tangerang'},
            {'name': 'PT Packpro (Packaging)', 'supplier_rank': 1, 'phone': '+62 21 777 8888', 'email': 'sales@packpro.id', 'street': 'Bekasi'},
        ]
        for p in partners:
            partner = env['res.partner'].search([('name', '=', p['name'])])
            if not partner:
                partner = env['res.partner'].create(p)
                print(f"  → {p['name']} created")
            else:
                print(f"  ✓ {p['name']} exists")
        print("  ✓ Partners done")

        print("[5/6] Create Users...")
        # Find group IDs
        sale_group = env['res.groups'].search([('name', '=', 'User')]).filtered(lambda g: 'sale' in str(g.name).lower() or hasattr(g, 'implied_ids'))

        users = [
            {'name': 'Marketing', 'login': 'marketing@duanaga.co.id', 'groups_id': [(5, 0)]},  # Basic user
            {'name': 'Produksi Manager', 'login': 'produksi@duanaga.co.id', 'groups_id': [(5, 0)]},
            {'name': 'QC Supervisor', 'login': 'qc@duanaga.co.id', 'groups_id': [(5, 0)]},
            {'name': 'Gudang Staff', 'login': 'gudang@duanaga.co.id', 'groups_id': [(5, 0)]},
            {'name': 'Purchasing', 'login': 'purchasing@duanaga.co.id', 'groups_id': [(5, 0)]},
        ]
        for u in users:
            user = env['res.users'].search([('login', '=', u['login'])])
            if not user:
                user = env['res.users'].create({
                    'name': u['name'],
                    'login': u['login'],
                    'password': 'Duanaga@2024',
                    'groups_id': u['groups_id'],
                })
                print(f"  → {u['name']} ({u['login']}) created")
            else:
                print(f"  ✓ {u['name']} exists")
        print("  ✓ Users done")

        print("[6/6] Create Warehouses...")
        warehouse = env['stock.warehouse'].search([('name', 'ilike', 'Dua Naga')])
        if not warehouse:
            warehouse = env['stock.warehouse'].create({
                'name': 'Dua Naga Main Warehouse',
                'code': 'DNWH1',
            })
            print("  → Warehouse created")
        else:
            print("  ✓ Warehouse exists")
        print("  ✓ Warehouses done")

        cr.commit()

    print("\n" + "=" * 50)
    print("✓ SETUP SELESAI!")
    print("=" * 50)
    print("\nBuka: http://localhost:8069")
    print("Login: admin / admin")

if __name__ == '__main__':
    setup_all()
