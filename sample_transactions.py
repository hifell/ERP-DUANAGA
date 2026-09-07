#!/usr/bin/env python3
"""
Sample Data untuk Latihan - PT Dua Naga Kosmetindo
Buat Sales Order, Purchase Order, Manufacturing Order sebagai contoh
"""
import odoo
odoo.tools.config['database'] = 'duanaga'

from odoo import api, SUPERUSER_ID
import odoo.modules.registry

registry = odoo.modules.registry.Registry('duanaga')

def create_sample_transactions():
    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})

        print("=" * 60)
        print("MEMBUAT SAMPLE TRANSAKSI UNTUK LATIHAN")
        print("=" * 60)

        # ===== 1. SALES ORDER =====
        print("\n[1] Membuat Sales Order...")

        customer = env['res.partner'].search([('name', '=', 'Beauty Glow Indonesia')], limit=1)
        product = env['product.product'].search([('default_code', '=', 'FG-SERM')], limit=1)

        if customer and product:
            so = env['sale.order'].create({
                'partner_id': customer.id,
                'partner_invoice_id': customer.id,
                'partner_shipping_id': customer.id,
                'order_line': [(0, 0, {
                    'product_id': product.id,
                    'product_uom_qty': 500,
                    'price_unit': product.list_price,
                })],
                'note': 'Private Label - Custom Bottle + Box with Logo',
            })
            so.action_confirm()
            print(f"  ✓ Sales Order Created: {so.name}")
            print(f"    Customer: {customer.name}")
            print(f"    Product: {product.name}")
            print(f"    Qty: 500 pcs")
        else:
            print("  ✗ Customer atau Product tidak ditemukan")

        # ===== 2. PURCHASE ORDER =====
        print("\n[2] Membuat Purchase Order...")

        supplier = env['res.partner'].search([('name', '=', 'CV Chemindo Sentosa')], limit=1)
        vitamin_c = env['product.product'].search([('default_code', '=', 'BB-VITC')], limit=1)
        glycerin = env['product.product'].search([('default_code', '=', 'BB-GLYC')], limit=1)

        if supplier and vitamin_c and glycerin:
            po = env['purchase.order'].create({
                'partner_id': supplier.id,
                'order_line': [
                    (0, 0, {
                        'product_id': vitamin_c.id,
                        'product_qty': 25,
                        'price_unit': vitamin_c.list_price,
                    }),
                    (0, 0, {
                        'product_id': glycerin.id,
                        'product_qty': 50,
                        'price_unit': glycerin.list_price,
                    }),
                ],
            })
            po.button_confirm()
            print(f"  ✓ Purchase Order Created: {po.name}")
            print(f"    Supplier: {supplier.name}")
            print(f"    - Vitamin C Powder: 25 kg")
            print(f"    - Glycerin USP: 50 kg")

            # Create Receipt
            print("  → Creating Receipt...")
            picking = env['stock.picking'].search([
                ('purchase_id', '=', po.id),
                ('picking_type_id.code', '=', 'incoming')
            ], limit=1)
            if picking:
                picking.action_assign()
                picking.button_validate()
                print(f"  ✓ Receipt Validated - Stock Updated")
        else:
            print("  ✗ Supplier atau Product tidak ditemukan")

        # ===== 3. MANUFACTURING ORDER =====
        print("\n[3] Membuat Manufacturing Order...")

        fg_product = env['product.product'].search([('default_code', '=', 'FG-SERM')], limit=1)

        if fg_product:
            # Get BoM
            bom = env['mrp.bom'].search([
                ('product_id', '=', fg_product.id),
                ('type', '=', 'normal')
            ], limit=1)

            if bom:
                mo = env['mrp.production'].create({
                    'product_id': fg_product.id,
                    'bom_id': bom.id,
                    'product_qty': 200,
                    'product_uom_id': bom.product_uom_id.id,
                })
                mo.action_confirm()
                print(f"  ✓ Manufacturing Order Created: {mo.name}")
                print(f"    Product: {fg_product.name}")
                print(f"    Qty: 200 pcs")

                # Mark as done (simulate production)
                print("  → Marking as Done...")
                mo.button_mark_done()
                print(f"  ✓ MO Completed - Finish Goods in Stock")
            else:
                print("  ✗ Bill of Materials tidak ditemukan")
        else:
            print("  ✗ Product tidak ditemukan")

        # ===== 4. DELIVERY ORDER =====
        print("\n[4] Membuat Delivery Order...")

        so_deliver = env['sale.order'].search([('name', '=', so.name)], limit=1) if 'so' in dir() else None
        if so_deliver:
            picking = env['stock.picking'].search([
                ('sale_id', '=', so_deliver.id),
                ('picking_type_id.code', '=', 'outgoing')
            ], limit=1)
            if picking:
                picking.action_assign()
                picking.button_validate()
                print(f"  ✓ Delivery Order Validated")
                print(f"    Delivered to: {customer.name}")
            else:
                print("  - Delivery sudah diproses atau belum ada")
        else:
            print("  - Sales Order tidak ditemukan")

        cr.commit()

    print("\n" + "=" * 60)
    print("✓ SAMPLE TRANSAKSI SELESAI!")
    print("=" * 60)
    print("\nCek hasil di Odoo:")
    print("  - Sales: Menu Sales → Orders")
    print("  - Purchase: Menu Purchase → Orders")
    print("  - Manufacturing: Menu Manufacturing → Orders")
    print("  - Inventory: Menu Inventory → Overview")

if __name__ == '__main__':
    create_sample_transactions()
