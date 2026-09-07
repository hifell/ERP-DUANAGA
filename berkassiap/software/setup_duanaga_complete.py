#!/usr/bin/env python3
"""
Complete Setup PT Dua Naga Kosmetindo
Maklon Cosmetics ERP
"""
import odoo
odoo.tools.config['database'] = 'duanaga'
odoo.tools.config['without_demo'] = True

from odoo import api, SUPERUSER_ID
import odoo.modules.registry

registry = odoo.modules.registry.Registry('duanaga')

def setup_duanaga():
    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})

        print("=" * 60)
        print("PT DUA NAGA KOSMETINDO - ERP SETUP")
        print("=" * 60)

        # ===== WAREHOUSES & LOCATIONS =====
        print("\n[1/8] Setting up Warehouses & Locations...")

        # Main warehouse
        warehouse = env['stock.warehouse'].search([('code', '=', 'DNWH1')])
        if not warehouse:
            warehouse = env['stock.warehouse'].create({
                'name': 'Dua Naga Main Warehouse',
                'code': 'DNWH1',
                'partner_id': 1,
            })
            print("  → Main warehouse created")
        else:
            print("  ✓ Main warehouse exists")

        # Create sub-locations
        locations = [
            ('WH/Stock/BB', 'Bahan Baku', 'internal'),
            ('WH/Stock/PK', 'Packaging', 'internal'),
            ('WH/Stock/FG', 'Finish Goods', 'internal'),
            ('WH/QC', 'Quality Control', 'internal'),
            ('WH/Produksi', 'Production Area', 'internal'),
            ('WH/Output', 'Finished Products', 'internal'),
        ]

        for code, name, usage in locations:
            loc = env['stock.location'].search([('complete_name', '=', code)])
            if not loc:
                parent = warehouse.lot_stock_id
                loc = env['stock.location'].create({
                    'name': name,
                    'complete_name': code,
                    'location_id': parent.id,
                    'usage': usage,
                })
                print(f"  → {code} created")
            else:
                print(f"  ✓ {code} exists")

        # ===== PRODUCT TEMPLATES WITH BoM =====
        print("\n[2/8] Creating Products with Bill of Materials...")

        # Get categories
        cat_bb = env['product.category'].search([('name', '=', 'Bahan Baku')])
        cat_pk = env['product.category'].search([('name', '=', 'Packaging')])
        cat_fc = env['product.category'].search([('name', '=', 'Face Care')])

        # Create raw materials if not exist
        materials = [
            ('BB-VITC', 'Vitamin C Powder (Raw)', cat_bb.id, 500000),
            ('BB-SHEA', 'Shea Butter (Raw)', cat_bb.id, 350000),
            ('BB-GLYC', 'Glycerin USP (Raw)', cat_bb.id, 180000),
            ('BB-NIAC', 'Niacinamide Powder', cat_bb.id, 420000),
            ('BB-HYAL', 'Hyaluronic Acid', cat_bb.id, 850000),
            ('BB-Aloe', 'Aloe Vera Extract', cat_bb.id, 280000),
            ('BB-SPF', 'SPF Booster Compound', cat_bb.id, 650000),
        ]

        material_ids = {}
        for code, name, cat, price in materials:
            prod = env['product.product'].search([('default_code', '=', code)])
            if not prod:
                prod = env['product.product'].create({
                    'name': name,
                    'default_code': code,
                    'categ_id': cat,
                    'type': 'consu',
                    'list_price': price,
                    'uom_id': 1,  # Units
                })
                print(f"  → {name} created")
            else:
                print(f"  ✓ {name} exists")
            material_ids[code] = prod.id

        # Create packaging
        packaging = [
            ('PK-BOT30', 'Botol Serum 30ml', cat_pk.id, 3500),
            ('PK-BOT50', 'Botol Lotion 50ml', cat_pk.id, 5000),
            ('PK-PUMP', 'Pump Dispenser', cat_pk.id, 2000),
            ('PK-CAP', 'Screw Cap', cat_pk.id, 800),
            ('PK-BOX', 'Box Packaging', cat_pk.id, 2500),
        ]

        pack_ids = {}
        for code, name, cat, price in packaging:
            prod = env['product.product'].search([('default_code', '=', code)])
            if not prod:
                prod = env['product.product'].create({
                    'name': name,
                    'default_code': code,
                    'categ_id': cat,
                    'type': 'consu',
                    'list_price': price,
                })
                print(f"  → {name} created")
            else:
                print(f"  ✓ {name} exists")
            pack_ids[code] = prod.id

        # Create Finish Goods with BoM
        print("\n  Creating Finish Goods with BoM...")
        finish_goods = [
            ('FG-SERM', 'Face Serum Vitamin C 30ml', cat_fc.id, 85000, 'FG-SERM-BOM'),
            ('FG-LOTO', 'Body Lotion Whitening 100ml', 4, 65000, 'FG-LOTO-BOM'),  # Body Care
            ('FG-SHMP', 'Hair Shampoo 200ml', 5, 45000, 'FG-SHMP-BOM'),  # Hair Care
        ]

        for code, name, cat_id, price, bom_name in finish_goods:
            # Create product
            prod = env['product.product'].search([('default_code', '=', code)])
            if not prod:
                prod = env['product.product'].create({
                    'name': name,
                    'default_code': code,
                    'categ_id': cat_id,
                    'type': 'product',  # Storable
                    'list_price': price,
                })
                print(f"  → {name} created")
            else:
                print(f"  ✓ {name} exists")

            # Create BoM
            bom = env['mrp.bom'].search([
                ('product_tmpl_id', '=', prod.product_tmpl_id.id),
                ('type', '=', 'normal')
            ])
            if not bom:
                # Get location
                stock_loc = env['stock.location'].search([('complete_name', '=', 'WH/Stock/FG')])
                warehouse_id = env['stock.warehouse'].search([('code', '=', 'DNWH1')])

                bom = env['mrp.bom'].create({
                    'product_tmpl_id': prod.product_tmpl_id.id,
                    'product_id': prod.id,
                    'product_qty': 1,
                    'product_uom_id': 1,
                    'type': 'normal',
                    'bom_line_ids': [
                        (0, 0, {'product_id': material_ids['BB-VITC'], 'product_qty': 0.5, 'product_uom_id': 1}),
                        (0, 0, {'product_id': material_ids['BB-GLYC'], 'product_qty': 1.0, 'product_uom_id': 1}),
                        (0, 0, {'product_id': material_ids['BB-NIAC'], 'product_qty': 0.3, 'product_uom_id': 1}),
                    ],
                    'byproduct_ids': [],
                })
                print(f"    → BoM created for {name}")
            else:
                print(f"    ✓ BoM exists for {name}")

        # ===== SUPPLIERS & CUSTOMERS =====
        print("\n[3/8] Setting up Partners...")

        suppliers = [
            ('SUP-CHEM', 'CV Chemindo Sentosa', 'Bahan Kimia', '+62 21 5551234', 'Tangerang'),
            ('SUP-PACK', 'PT Packpro Indonesia', 'Packaging', '+62 21 7778888', 'Bekasi'),
            ('SUP-LAB', 'CV Lab Supplies', 'Alat Lab', '+62 21 3334444', 'Jakarta'),
            ('SUP-RAW', 'PT Raw Material Indonesia', 'Bahan Baku Kosmetik', '+62 31 8889999', 'Surabaya'),
        ]

        for code, name, category, phone, city in suppliers:
            partner = env['res.partner'].search([('name', '=', name)])
            if not partner:
                partner = env['res.partner'].create({
                    'name': name,
                    'supplier_rank': 1,
                    'phone': phone,
                    'street': city,
                    'comment': category,
                })
                print(f"  → Supplier: {name}")
            else:
                print(f"  ✓ Supplier: {name}")

        customers = [
            ('CUS-BGLO', 'Beauty Glow Indonesia', 'Skincare Brand', 'Jakarta'),
            ('CUS-SKLB', 'SkinLab Clinic', 'Clinic', 'Jakarta'),
            ('CUS-SPA', 'Spa Serenity Bali', 'Spa', 'Bali'),
            ('CUS-HTL', 'Hotel Bintang Group', 'Hotel', 'Surabaya'),
            ('CUS-PRV', 'Private Label Client', 'Private Label', 'Various'),
        ]

        for code, name, category, city in customers:
            partner = env['res.partner'].search([('name', '=', name)])
            if not partner:
                partner = env['res.partner'].create({
                    'name': name,
                    'customer_rank': 1,
                    'street': city,
                    'comment': category,
                })
                print(f"  → Customer: {name}")
            else:
                print(f"  ✓ Customer: {name}")

        # ===== PROJECTS (R&D Formula Development) =====
        print("\n[4/8] Creating R&D Projects...")

        projects = [
            ('R&D Skincare 2024', 'New Skincare Product Development', 'Skincare'),
            ('R&D Haircare 2024', 'New Haircare Product Development', 'Haircare'),
            ('Formula Improvement', 'Cost Optimization & Efficacy', 'Internal'),
        ]

        for name, description, category in projects:
            proj = env['project.project'].search([('name', '=', name)])
            if not proj:
                proj = env['project.project'].create({
                    'name': name,
                    'description': description,
                })
                print(f"  → Project: {name}")
            else:
                print(f"  ✓ Project: {name}")

        # ===== STOCK RULES =====
        print("\n[5/8] Setting up Stock Rules...")

        # Get warehouse
        warehouse = env['stock.warehouse'].search([('code', '=', 'DNWH1')])
        if warehouse:
            # Set routes
            warehouse.write({
                'reception_steps': 'three_steps',  # Receive -> QC -> Stock
                'delivery_steps': 'pick_pack_ship',
            })
            print("  ✓ Warehouse routes configured")

        # ===== SEQUENCES =====
        print("\n[6/8] Configuring Sequences...")

        sequences_to_update = [
            ('stock.picking', 'DN'),
            ('purchase.order', 'PO'),
            ('sale.order', 'SO'),
        ]

        for model, prefix in sequences_to_update:
            seq = env['ir.sequence'].search([('code', '=', f'{model}')])
            if seq:
                seq.write({'prefix': f'{prefix}/%(year)s/', 'padding': 5})
                print(f"  ✓ {model} sequence updated")
            else:
                print(f"  - {model} sequence not found")

        # ===== QUALITY CHECKS =====
        print("\n[7/8] Setting up Quality Controls...")

        print("  → Note: Quality Control module (quality_control) not available")
        print("  → QC can be done via Inventory > Quality Checks")

        # ===== DASHBOARD WIDGETS =====
        print("\n[8/8] Setting up Dashboard...")

        print("  ✓ Dashboard ready (Odoo 17 auto-generates)")

        # Commit all
        cr.commit()

    print("\n" + "=" * 60)
    print("✓ COMPLETE SETUP DONE!")
    print("=" * 60)
    print("\nSummary:")
    print("  - Warehouses: 1 main warehouse with sub-locations")
    print("  - Products: Raw materials, Packaging, Finish Goods")
    print("  - BoM: Bill of Materials for production")
    print("  - Partners: Suppliers & Customers")
    print("  - Projects: R&D formula development")
    print("  - Stock: Receipt, QC, Delivery rules")
    print("\nNext Steps:")
    print("  1. Create Purchase Orders for raw materials")
    print("  2. Receive materials in Inventory")
    print("  3. Create Manufacturing Orders")
    print("  4. Create Sales Orders")
    print("\nURL: http://localhost:8069")
    print("Login: admin / admin")

if __name__ == '__main__':
    setup_duanaga()
