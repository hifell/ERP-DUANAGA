# PANDUAN TESTING ERP PT DUA NAGA KOSMETINDO

**Versi:** 2.0
**Tanggal:** 14 September 2026
**Database:** duanaga
**URL:** http://localhost:8069

---

## LOGIN

```
Database: duanaga
Username: admin
Password: admin123
```

---

## MODUL 1: SALES (PENJUALAN)

### Menu Actual:
```
Sales (sidebar kiri)
├── Quotations              ← Klik untuk buat quotation
├── My Quotations
├── Orders to Invoice
├── Orders to Upsell
├── Orders
└── Sales Teams
```

---

### SCENARIO 1.1: Buat Quotation untuk Toko Kosmetik

**Tujuan:** Buat penawaran harga untuk customer baru

**Langkah:**
1. Menu: **Sales → Quotations**
2. Klik tombol: **Create**
3. Isi form lengkap:

```
═══════════════════════════════════════════════════════
FORM QUOTATION
═══════════════════════════════════════════════════════

CUSTOMER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Customer:        Toko Kosmetik Melawai
Email:           sales@tokomelawai.com
Phone:           021-7654321
Delivery Address: Jl. Melawai No. 88, Jakarta Selatan

ORDER LINES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Add product] ← Klik link ini

┌─────────────────────────────────────────────────────┐
│ Add a Product                                       │
├─────────────────────────────────────────────────────┤
│ Product:           Sabun Wajah GlowUp              │
│ Quantity:          500                              │
│ Unit:              Pcs                              │
│ Unit Price (Rp):   25.000                           │
│ Taxes:             None                             │
│ Subtotal:          Rp 12.500.000                     │
└─────────────────────────────────────────────────────┘

[Add another product]

┌─────────────────────────────────────────────────────┐
│ Product:           Lip Cream Matte #03              │
│ Quantity:          200                              │
│ Unit:              Pcs                              │
│ Unit Price (Rp):   35.000                           │
│ Taxes:             None                             │
│ Subtotal:          Rp 7.000.000                     │
└─────────────────────────────────────────────────────┘

DELIVERY DATE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Delivery Date:    25/09/2026

PAYMENT TERMS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Payment Terms:    30 Days

NOTES (Optional)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Terms & Conditions:
- Harga sudah termasuk PPN
- Free ongkir untuk pembelian > Rp 10.000.000
- Min. order: 100 pcs per SKU
- Lead time: 14 hari kerja

═══════════════════════════════════════════════════════
```

4. Klik: **Save**
5. Lihat hasil:
   - Quotation number: SOO/xxxx/xxxxx
   - Total: Rp 19.500.000
   - Status: **Quotation**

**Hasil Test:**
- [ ] Quotation tersimpan
- [ ] Total price Kalkulasi otomatis
- [ ] Bisa edit/edit ulang

---

### SCENARIO 1.2: Konfirmasi Quotation jadi Sales Order

**Langkah:**
1. Buka quotation yang sudah dibuat (SOO/xxxx/xxxxx)
2. Klik tombol: **Confirm Sale** (warna hijau)
3. Konfirmasi popup

**Hasil:**
```
Status berubah: Quotation → Sales Order
Tanggal confirm: 14/09/2026
Expected delivery: 25/09/2026
```

**Hasil Test:**
- [ ] Status berubah jadi "Sales Order"
- [ ] Tombol "Create Invoice" muncul
- [ ] Tombol "Delivery" muncul

---

### SCENARIO 1.3: Buat Quotation Wholesale untuk Distributor

**Langkah:**
1. Menu: **Sales → Quotations**
2. Klik: **Create**
3. Isi:

```
═══════════════════════════════════════════════════════
CUSTOMER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Customer:        PT Kosmetik Jaya Abadi
Email:           purchasing@kosmetikjaya.co.id
Phone:           021-8888888
Delivery Address: Gudang KJ, Jl. Industri Raya No. 15, Jakarta

ORDER LINES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌─────────────────────────────────────────────────────┐
│ Product:           Paket Skincare Bundling          │
│ Description:       Paket lengkap skincare 5-in-1   │
│ Quantity:          100                              │
│ Unit:              Box                             │
│ Unit Price (Rp):   250.000                          │
│ Discount:          15%                            │
│ Subtotal:          Rp 21.250.000                     │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ Product:           Serum Whitening Premium         │
│ Quantity:          300                              │
│ Unit:              Pcs                             │
│ Unit Price (Rp):   85.000                           │
│ Discount:          10%                            │
│ Subtotal:          Rp 22.950.000                     │
└─────────────────────────────────────────────────────┘

PAYMENT TERMS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Payment Terms:    50% DP, 50% sebelum kirim

DELIVERY DATE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Delivery Date:    05/10/2026

NOTES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Free booth untuk event launches
- Support marketing materials
- Priority production schedule
- Harga EXW Jakarta (belum termasuk ongkir)

═══════════════════════════════════════════════════════
```

**Hasil Test:**
- [ ] Diskon Kalkulasi otomatis
- [ ] Total: Rp 44.200.000

---

## MODUL 2: PURCHASING (PEMBELIAN)

### Menu Actual:
```
Purchase (sidebar kiri)
├── Purchase Orders          ← Lihat PO
├── Requests for Quotation  ← RFQ untuk minta quotation vendor
├── ...
```

---

### SCENARIO 2.1: Buat Request for Quotation (RFQ)

**Tujuan:** Minta quotation harga dari supplier

**Langkah:**
1. Menu: **Purchase → Requests for Quotation**
2. Klik: **Create**
3. Isi:

```
═══════════════════════════════════════════════════════
FORM RFQ
═══════════════════════════════════════════════════════

VENDOR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Vendor:          PT Chemindo Maju
Email:           sales@chemindo.co.id
Vendor Address:  Jl. Industri Kimia No. 45, Tangerang

ORDER LINES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌─────────────────────────────────────────────────────┐
│ Product:           Glycerin 99% (Pharmaceutical)   │
│ Quantity:          500                              │
│ Unit:              kg                              │
│ Description:       Glycerin grade kosmetik         │
│ Expected Price:   [kosong - vendor isi]           │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ Product:           Kojic Acid                       │
│ Quantity:          50                               │
│ Unit:              kg                              │
│ Description:       Kojic acid powder BPOM grade   │
│ Expected Price:   [kosong - vendor isi]           │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ Product:           Niacinamide USP                  │
│ Quantity:          30                               │
│ Unit:              kg                              │
│ Description:       Niacinamide powder              │
│ Expected Price:   [kosong - vendor isi]           │
└─────────────────────────────────────────────────────┘

DELIVERY DATE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Confirmation Date:  18/09/2026
Deadline:           30/09/2026

NOTES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Sertakan COA (Certificate of Analysis)
- Sertakan SDS (Safety Data Sheet)
- Kemasan: 25kg/drum
- Expiry min. 2 tahun

═══════════════════════════════════════════════════════
```

4. Klik: **Send by Email** (opsional - kirim RFQ ke vendor)
5. Klik: **Save**

**Hasil Test:**
- [ ] RFQ tersimpan
- [ ] Bisa kirim email ke vendor

---

### SCENARIO 2.2: Buat Purchase Order dari RFQ

**Langkah:**
1. Buka RFQ yang sudah dibuat
2. Klik: **Confirm Order**
3. Popup konfirmasi → Klik **Ok**

**Hasil:**
```
Status berubah: RFQ → Purchase Order
PO Number: POO/xxxx/xxxxx
Vendor: PT Chemindo Maju
Total Estimated: Rp 45.000.000 (estimasi)

Tanggal Confirm: 14/09/2026
Expected Delivery: 30/09/2026
```

---

### SCENARIO 2.3: Terima Barang dari PO

**Langkah:**
1. Buka PO yang sudah di-confirm
2. Klik tab: **Receipts**
3. Klik: **Receive Products**
4. Isi quantity yang diterima:

```
┌─────────────────────────────────────────────────────┐
│ Receive Products                                    │
├─────────────────────────────────────────────────────┤
│ Glycerin 99%                                       │
│ Ordered:    500 kg                                 │
│ Received:   500 kg      ← Edit sesuai diterima   │
│ Condition:  ✅ Good                                │
├─────────────────────────────────────────────────────┤
│ Kojic Acid                                       │
│ Ordered:    50 kg                                 │
│ Received:   50 kg                                 │
│ Condition:  ✅ Good                                │
├─────────────────────────────────────────────────────┤
│ Niacinamide USP                                   │
│ Ordered:    30 kg                                 │
│ Received:   30 kg                                 │
│ Condition:  ✅ Good                                │
└─────────────────────────────────────────────────────┘
```

5. Klik: **Validate**

**Hasil:**
```
Receipt Number: WH/IN/xxxx/xxxxx
Status: Done
Stock Glycerin: +500 kg
Stock Kojic Acid: +50 kg
Stock Niacinamide: +30 kg
```

**Hasil Test:**
- [ ] Stock bertambah di inventory
- [ ] PO status: "Received"

---

## MODUL 3: INVENTORY (GUDANG)

### Menu Actual:
```
Inventory (sidebar kiri)
├── Orders                     ← Delivery orders
├── Products                   ← Lihat semua produk
│   ├── Products              ← Klik ini
│   ├── Product Categories
│   └── Product Attributes
├── Reordering Rules         ← Atur reorder point
├── ...
```

---

### SCENARIO 3.1: Lihat Stock Produk

**Langkah:**
1. Menu: **Inventory → Products → Products**
2. Klik salah satu produk
3. Lihat informasi:

```
═══════════════════════════════════════════════════════
PRODUCT: Sabun Wajah GlowUp
═══════════════════════════════════════════════════════

GENERAL INFORMATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Product Type:        Storable Product
Category:           Skincare / Kosmetik
Barcode:            8991234567890
Unit of Measure:   Pcs

SALES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Sale Price:        Rp 25.000
Can be sold:        ✅ Yes

PURCHASING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Cost:               Rp 9.500
Can be purchased:   ✅ Yes
Vendor:             PT Chemindo Maju

INVENTORY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Quantity On Hand:        1.250 Pcs
Reserved Quantity:          500 Pcs
Forecasted Quantity:       750 Pcs
```

---

### SCENARIO 3.2: Buat Delivery Order

**Langkah:**
1. Menu: **Inventory → Orders**
2. Klik: **Create**
3. Isi:

```
═══════════════════════════════════════════════════════
FORM DELIVERY ORDER
═══════════════════════════════════════════════════════

DELIVERY ORDER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Operation Type:    Delivery Orders
Customer:          Toko Kosmetik Melawai
Scheduled Date:    25/09/2026
Source Document:  SOO/2026/0012

DELIVERY LINES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌─────────────────────────────────────────────────────┐
│ Product:           Sabun Wajah GlowUp              │
│ Quantity:          500                              │
│ Unit:              Pcs                             │
│ Available:         1.250 Pcs (sufficient)         │
└─────────────────────────────────────────────────────┘

INTERNAL NOTES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Prioritas kirim besok pagi
- Hubungi Pak Budi sebelum antar: 081234567890
- Packaging: 50pcs/plastic bag, 10 bags/box

═══════════════════════════════════════════════════════
```

4. Klik: **Validate** (tombol √ hijau)

**Hasil:**
```
Delivery Order: DOO/xxxx/xxxxx
Status: Done
Stock After: 750 Pcs (1.250 - 500)

Journal Entry Created:
- Stock Destination: Customer
- Quantity: 500 Pcs
```

**Hasil Test:**
- [ ] Stock berkurang
- [ ] Customer delivery recorded

---

### SCENARIO 3.3: Atur Reorder Point

**Langkah:**
1. Menu: **Inventory → Reordering Rules**
2. Klik: **Create**
3. Isi:

```
═══════════════════════════════════════════════════════
REORDERING RULE
═══════════════════════════════════════════════════════

PRODUCT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Product:          Glycerin 99%

VENDOR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Vendor:          PT Chemindo Maju

ORDERING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Minimum Quantity:    100 kg     ← Trigger point
Maximum Quantity:   500 kg     ← Order sampai max
Quantity Multiple:  50 kg      ← Kelipatan order

POLICY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Trigger:          On Hand + Incoming ≤ Minimum
Order Frequency:  Weekly
```

4. Klik: **Save**

**Hasil Test:**
- [ ] Jika Glycerin ≤ 100kg, sistem alert
- [ ] Purchase Request auto-created

---

## MODUL 4: MANUFACTURING (PRODUKSI)

### Menu Actual:
```
Manufacturing (sidebar kiri)
├── Manufacturing Orders     ← Klik untuk MO
├── Work Orders
├── Products                   ← Products dengan BoM
│   ├── Products              ← Klik ini
│   └── Product Variants
├── Bills of Materials        ← Lihat/buat BoM
├── ...
```

---

### SCENARIO 4.1: Buat Manufacturing Order (MO)

**Langkah:**
1. Menu: **Manufacturing → Manufacturing Orders**
2. Klik: **Create**
3. Isi:

```
═══════════════════════════════════════════════════════
FORM MANUFACTURING ORDER
═══════════════════════════════════════════════════════

PRODUCTION ORDERS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Product to Produce:  Sabun Wajah GlowUp
Quantity:            500 Pcs
Bill of Material:     Sabun Wajah GlowUp - Default

SCHEDULING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Deadline Start Date:  20/09/2026
                       (auto-calculated)

AVAILABLE COMPONENTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Glycerin 99%:       75 kg    ✅ Available
Kojic Acid:         25 kg    ✅ Available
Niacinamide:        15 kg    ✅ Available
Aqua:              300 kg    ✅ Available

OPERATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Workcenter:         Mixing Station
Workcenter:         Filling Line
Workcenter:         Packaging

═══════════════════════════════════════════════════════
```

4. Klik: **Save**
5. Klik: **Confirm**
6. Klik: **Mark as Started**

**Hasil:**
```
MO Number: MO/2026/09/0025
Status: In Progress
Product: Sabun Wajah GlowUp
Quantity: 500 Pcs
Deadline: 20/09/2026
```

---

### SCENARIO 4.2: Produksi Selesai (Create Finished)

**Langkah:**
1. Buka MO yang sedang berjalan
2. Klik tab: **Work Orders**
3. Klik: **Mark as Done** untuk setiap work order

```
Work Order 1: Mixing Station
Status: ✅ Done

Work Order 2: Filling Line
Status: ✅ Done

Work Order 3: Packaging
Status: ✅ Done
```

4. Klik: **Produce** (atau "Mark as Done" di MO)
5. Isi quantity finished:

```
┌─────────────────────────────────────────────────────┐
│ Quantity:        500 Pcs                           │
│ Lot/Serial No.: LOT-2026-0914-001                 │
│ Location:        Production / Stock               │
└─────────────────────────────────────────────────────┘
```

6. Klik: **Ok**

**Hasil:**
```
MO Number: MO/2026/09/0025
Status: Done
Qty Produced: 500 Pcs
Finished Products Location: WH/Stock

Stock Update:
- Sabun Wajah GlowUp: +500 Pcs
```

**Hasil Test:**
- [ ] MO status: "Done"
- [ ] Stock produk jadi bertambah

---

### SCENARIO 4.3: Buat Bill of Materials (BoM)

**Langkah:**
1. Menu: **Manufacturing → Bills of Materials**
2. Klik: **Create**
3. Isi:

```
═══════════════════════════════════════════════════════
FORM BILL OF MATERIALS
═══════════════════════════════════════════════════════

BILL OF MATERIALS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Product:           Sabun Anti Aging Premium
Reference:        BoM-SABUN-AGING-001
BoM Type:         Manufacture this product
```

4. Tab **Components** → Add:

```
┌─────────────────────────────────────────────────────┐
│ PRODUCT              │ QTY     │ UNIT │ COST/UNIT  │
├─────────────────────────────────────────────────────┤
│ Aqua                 │ 60.000  │ kg   │ Rp 5.000   │
│ Glycerin 99%         │ 15.000  │ kg   │ Rp 45.000  │
│ Collagen Powder      │ 5.000   │ kg   │ Rp 350.000 │
│ Vitamin E Oil       │ 3.000   │ kg   │ Rp 280.000  │
│ Niacinamide          │ 3.000   │ kg   │ Rp 500.000  │
│ Fragrance "Anti Aging"│ 2.000 │ kg   │ Rp 200.000  │
│ Preservative Euxyl  │ 0.500   │ kg   │ Rp 150.000  │
│ Colorant Beige      │ 0.200   │ kg   │ Rp 100.000  │
└─────────────────────────────────────────────────────┘

Subtotal Material: Rp 4.450.000 per batch
Batch Size: 100 kg → 500 pcs
```

5. Tab **Work Orders** → Add:

```
┌─────────────────────────────────────────────────────┐
│ WORKCENTER         │ TIME    │ DESCRIPTION         │
├─────────────────────────────────────────────────────┤
│ Mixing Station      │ 30 min  │ Campurkan semua    │
│                      │         │ bahan, homogenkan  │
├─────────────────────────────────────────────────────┤
│ Heating Tank        │ 45 min  │ Panaskan 45°C,    │
│                      │         │ aduk kontinu       │
├─────────────────────────────────────────────────────┤
│ Filling Line        │ 60 min  │ Isi ke packaging,  │
│                      │         │ 500 pcs/batch      │
├─────────────────────────────────────────────────────┤
│ Quality Check       │ 15 min  │ Sample testing,    │
│                      │         │ pH & viscosity     │
└─────────────────────────────────────────────────────┘
```

6. Klik: **Save**

**Cost Analysis (Otomatis):**
```
═══════════════════════════════════════════════════════
COST BREAKDOWN - Sabun Anti Aging Premium
═══════════════════════════════════════════════════════

MATERIAL COST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Per Batch (100kg / 500pcs):
- Aqua:                 Rp 300.000
- Glycerin:            Rp 675.000
- Collagen:            Rp 1.750.000
- Vitamin E:           Rp 840.000
- Niacinamide:         Rp 1.500.000
- Fragrance:            Rp 400.000
- Preservative:        Rp 75.000
- Colorant:            Rp 20.000
─────────────────────────────────────────────────────
TOTAL MATERIAL:        Rp 5.560.000

MANUFACTURING COST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Labor (3 workers x 2.5hrs):    Rp 450.000
Overhead (listrik, air):      Rp 100.000
Packaging (500 pcs):           Rp 150.000
─────────────────────────────────────────────────────
TOTAL MFG COST:                Rp 700.000

GRAND TOTAL PER BATCH:         Rp 6.260.000
COST PER PCS (500 pcs):       Rp 12.520
═══════════════════════════════════════════════════════
```

**Hasil Test:**
- [ ] BoM tersimpan
- [ ] Cost Kalkulasi otomatis
- [ ] Bisa digunakan untuk MO

---

## MODUL 5: QUALITY CONTROL (QC)

### Menu Actual:
```
QC KBR System (sidebar kiri, setelah addon terinstall)
├── KBR Decisions              ← Lihat semua QC decisions
├── ...
```

---

### SCENARIO 5.1: QC Check - Approved

**Langkah:**
1. Menu: **Manufacturing → Manufacturing Orders**
2. Buka MO: **MO/2026/09/0025** (yang baru selesai diproduksi)
3. Di form MO, cari tombol: **Create QC Decision**
4. Klik tombol tersebut
5. Popup form QC - Isi:

```
═══════════════════════════════════════════════════════
FORM QC KBR DECISION
═══════════════════════════════════════════════════════

PRODUCTION INFO (Auto-filled)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Production Order:   MO/2026/09/0025
Batch ID:          LOT-2026-0914-001
Product:           Sabun Wajah GlowUp
Qty Produced:      500 Pcs

QC PARAMETERS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌─────────────────────────────────────────────────────┐
│ pH Level                                            │
│ Input:         6.1                                  │
│ Min:           5.5                                 │
│ Max:           6.5                                 │
│ Status:        ✅ IN RANGE                          │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ Viscosity                                           │
│ Input:         1.07                                 │
│ Min:           1.05                                 │
│ Max:           1.10                                 │
│ Status:        ✅ IN RANGE                          │
└─────────────────────────────────────────────────────┘

VISUAL CHECK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Color:           Sesuai standard   ✅
Odor:            Sesuai standard   ✅
Packaging:       Tidak rusak       ✅

QC ANALYST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Analyst:         QC Staff - Duanaga
Test Date:       14/09/2026
Test Time:       14:30

═══════════════════════════════════════════════════════
```

6. Klik: **Submit to KBR Engine**

**Hasil:**
```
═══════════════════════════════════════════════════════
KBR ENGINE DECISION
═══════════════════════════════════════════════════════

Status: ✅ APPROVED

pH In Range:           YES    (6.1 within 5.5-6.5)
Viscosity In Range:   YES    (1.07 within 1.05-1.10)

Recommendation:
"Batch memenuhi spesifikasi. 
Releasable untuk distribusi."

Qty Approved:          500 Pcs

═══════════════════════════════════════════════════════
```

**MO Otomatis Update:**
```
MO Status:    Done
Stock:        +500 Pcs ke Gudang
QC Decision:  1 record created
```

---

### SCENARIO 5.2: QC Check - Rework Required

**Langkah:**
1. Buka MO berbeda (misal: MO/2026/09/0020)
2. Klik **Create QC Decision**
3. Isi hasil lab:

```
QC PARAMETERS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌─────────────────────────────────────────────────────┐
│ pH Level                                            │
│ Input:         6.8         ← ❌ OUT OF RANGE      │
│ Min:           5.5                                 │
│ Max:           6.5                                 │
│ Status:        ❌ OUT OF RANGE                      │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ Viscosity                                           │
│ Input:         1.08         ✅ IN RANGE            │
│ Status:        ✅ IN RANGE                          │
└─────────────────────────────────────────────────────┘
```

4. Klik: **Submit to KBR Engine**

**Hasil:**
```
═══════════════════════════════════════════════════════
KBR ENGINE DECISION
═══════════════════════════════════════════════════════

Status: ⚠️ REWORK REQUIRED

pH In Range:           NO     (6.8 exceeds 6.5)
Viscosity In Range:     YES

Recommendation:
"pH terlalu tinggi (6.8).
Adjustment: tambah asam sitrat 0.5% 
lalu re-test."

Action Required:
1. Kembalikan ke Mixing Station
2. Tambahkan Asam Sitrat 0.5%
3. Homogenkan 15 menit
4. Re-test pH
5. Jika OK, resubmit QC

═══════════════════════════════════════════════════════
```

**MO Update:**
```
MO Status:    In Progress (kembali)
Reason:       Rework Required
```

---

### SCENARIO 5.3: QC Check - Rejected

**Langkah:**
1. QC check menunjukkan hasil buruk
2. Submit ke KBR Engine

**Hasil:**
```
═══════════════════════════════════════════════════════
KBR ENGINE DECISION
═══════════════════════════════════════════════════════

Status: ❌ REJECTED

Issue: Kontaminasi mikroba terdeteksi
Result: 500 CFU/g (limit: 100 CFU/g)

Recommendation:
"Batch gagal karena kontaminasi mikroba.
Destroy batch sesuai SOP waste management.
Investigasi root cause:
- Sanitasi equipment?
- Kualitas bahan baku?
- Hygiene персонал?"

Action Required:
1. Jangan distribute batch ini
2. Scarp sesuai SOP
3. Investigasi kontaminasi
4. Corrective action sebelum produksi berikutnya

═══════════════════════════════════════════════════════
```

**MO Update:**
```
MO Status:     Cancelled
Qty Approved:  0 Pcs
Waste Record:   Created
```

---

### SCENARIO 5.4: Lihat QC Dashboard

**Langkah:**
1. Menu: **QC KBR System → KBR Decisions**
2. Lihat semua QC decisions
3. Filter options:
   - Status: Approved / Rework / Rejected
   - Date range
   - Product

**Dashboard View:**
```
═══════════════════════════════════════════════════════
QC KBR DECISIONS DASHBOARD
═══════════════════════════════════════════════════════

SUMMARY (September 2026)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total QC:       25 Batch
Approved:       22 Batch (88%)   ✅
Rework:         2 Batch (8%)     ⚠️
Rejected:       1 Batch (4%)     ❌

PRODUCTIVITY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Avg Test Time:      45 menit/batch
First Pass Rate:    88%

═══════════════════════════════════════════════════════
```

---

## MODUL 6: REGULATORY (REGULASI BPOM)

### Menu Actual:
```
Regulatory (sidebar kiri, setelah addon terinstall)
├── Product Registrations
├── Ingredients
├── ...
```

---

### SCENARIO 6.1: Registrasi Produk Baru

**Langkah:**
1. Menu: **Regulatory → Product Registrations**
2. Klik: **Create**
3. Isi lengkap:

```
═══════════════════════════════════════════════════════
FORM PRODUCT REGISTRATION
═══════════════════════════════════════════════════════

BASIC INFORMATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Product Name:        Sabun Pemutih Wajah GlowUp Plus
Brand:               GlowUp
Product Category:    MLS (Make Up Lip Stain)
Net Weight:         100 gram
Packaging Type:     Sachet + Box

BPOM INFORMATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NIE Number:         [kosong - akan diisi BPOM]
NIE Status:         Pending Submission
Submission Date:    14/09/2026
License Number:     CPOB/DN/2024/089
License Expiry:    31/12/2027

INGREDIENTS (INCI FORMAT)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌─────────────────────────────────────────────────────┐
│ No │ Ingredient            │ Function      │ %     │
├─────────────────────────────────────────────────────┤
│ 1  │ Aqua                  │ Solvent       │ 60.0  │
│ 2  │ Glycerin              │ Humectant     │ 15.0  │
│ 3  │ Sodium Lauryl Sulfate │ Surfactant    │ 10.0  │
│ 4  │ Kojic Acid            │ Brightening   │ 1.0   │
│ 5  │ Niacinamide           │ Skin Care     │ 3.0   │
│ 6  │ Titanium Dioxide      │ UV Filter     │ 5.0   │
│ 7  │ Fragrance             │ Parfum        │ 2.0   │
│ 8  │ Phenoxyethanol        │ Preservative  │ 0.8   │
│ 9  │ Tocopheryl Acetate    │ Antioxidant   │ 1.0   │
│ 10 │ Allantoin              │ Soothing     │ 0.5   │
└─────────────────────────────────────────────────────┘
Total: 100%

⚠️ CAUTION:
- Kojic Acid: BPOM max 1% → ✅ OK (1.0%)
- Nikotinate: BPOM restricted → ❌ REMOVE

PRODUCT CLAIMS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Claim:              "Membantu mencerahkan kulit wajah"
Claim Category:      Peralatan Kecantikan
Warning Label:      "Hanya untuk pemakaian luar"
                      "Hindari kontak dengan mata"
                      "Simpan di tempat sejuk"

MANUFACTURER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Factory:            PT Dua Naga Kosmetindo
Address:            Jl. Industri Manufaktur No. 10
                      Kawasan Industri, Tangerang
CLA License:        CPOB/DN/2024/089

DOCUMENTS TO UPLOAD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] Certificate of Analysis (COA)
[ ] Formula/Composition Letter
[ ] Manufacturing Flow Chart
[ ] Label Design (Bahasa Indonesia)
[ ] BPOM Notification Letter
[ ] Letter of Authorization (if applicable)

═══════════════════════════════════════════════════════
```

4. Klik: **Save**

**Hasil Test:**
- [ ] Product registration tersimpan
- [ ] Status: "Pending Submission"

---

### SCENARIO 6.2: Tracking Status NIE

**Langkah:**
1. Menu: **Regulatory → Product Registrations**
2. Lihat dashboard / list

**Status Pipeline:**
```
═══════════════════════════════════════════════════════
BPOM REGISTRATION TRACKER
═══════════════════════════════════════════════════════

PRODUCT                    │ STATUS     │ NIE
─────────────────────────────────────────────────────
Sabun GlowUp Plus          │ 🔄 Pending │ -
Serum Vit C Premium        │ ✅ Approved│ ML12345678901AB
Lip Cream Matte #03        │ ✅ Approved│ ML98765432100ZZ
Night Cream Classic        │ ❌ EXPIRED│ ML55555555555YY
Lip Tint Natural           │ 🔄 Review │ ML11111111111AA

═══════════════════════════════════════════════════════
```

---

### SCENARIO 6.3: Ingredient Monitoring

**Langkah:**
1. Menu: **Regulatory → Ingredients**
2. Lihat monitored ingredients

**Alert View:**
```
═══════════════════════════════════════════════════════
INGREDIENT MONITORING
═══════════════════════════════════════════════════════

⚠️ CRITICAL - BANNED/RESTRICTED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌─────────────────────────────────────────────────────┐
│ Ingredient          │ Status    │ Max Limit │ Alert │
├─────────────────────────────────────────────────────┤
│ Mercury             │ ❌ BANNED│ 0%        │ STOP  │
│ Hydroquinone        │ ⚠️ LIMIT │ 2%        │ 1.5% │
│ Kojic Acid          │ ⚠️ LIMIT │ 1%        │ 0.8% │
│ Retinol             │ ⚠️ LIMIT │ 2.5%     │ 2.0% │
│ T Retinoate         │ ❌ BANNED│ 0%        │ STOP │
└─────────────────────────────────────────────────────┘

✅ SAFE IN CURRENT FORMULATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌─────────────────────────────────────────────────────┐
│ Ingredient          │ Status    │ Current Use│ Alert │
├─────────────────────────────────────────────────────┤
│ Niacinamide          │ ✅ OK    │ 3%        │ OK   │
│ Vitamin C            │ ✅ OK    │ 5%        │ OK   │
│ Glycerin             │ ✅ OK    │ 15%       │ OK   │
│ Titanium Dioxide     │ ✅ OK    │ 5%        │ OK   │
└─────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════
```

---

## MODUL 7: N8N WORKFLOWS

### Login n8n
```
URL: http://localhost:5678
Username: admin
Password: Duanaga@2024
```

---

### SCENARIO 7.1: Test Lead Capture Workflow

**Langkah:**
1. Login ke n8n
2. Klik **Workflows** di menu kiri
3. Cari workflow: **W1: Lead Capture Working**
4. Klik workflow tersebut
5. Klik: **Execute Workflow**
6. Test data:

```json
{
  "name": "Budi Santoso",
  "email": "budi@ptbudisentosa.com",
  "phone": "081234567890",
  "interest": "wholesale",
  "message": "Saya interested dengan produk Sabun Pemutih untuk diedarkan di area Surabaya. Bisa kirim katalog?"
}
```

7. Klik **Execute**
8. Cek apakah lead masuk ke Odoo:
   - Menu: **Sales → Leads** atau **Quotations**

---

### SCENARIO 7.2: Test Manual Webhook

**Langkah:**
1. Buka terminal / command prompt
2. Jalankan command:

```bash
curl -X POST http://localhost:5678/webhook-test/lead-capture \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "phone": "081234567890",
    "interest": "wholesale",
    "message": "Test message"
  }'
```

**Expected Response:**
```json
{"success": true}
```

3. Cek Odoo - lead harus muncul

---

### SCENARIO 7.3: Cek Active Workflows

**Langkah:**
1. Di n8n, klik **Workflows**
2. Lihat list semua workflows

**Expected Active Workflows:**
```
✅ W1: Lead Capture Working
✅ W1: Lead Capture XML-RPC
✅ W1: Lead Capture v2
✅ W2: Daily Report - Jam 08:00
✅ W3: Low Stock Alert - Jam 09:00
✅ W4: SO Confirmed - Alert Production
✅ W5: Delivery Done - Notify Customer
✅ W6: Invoice Reminder
✅ W7: Production Tracking
✅ W8: Customer Feedback Request
✅ W9: E-Commerce Order (Shopee/Tokopedia)
✅ BPOM Status WA Notification
```

---

## MODUL 8: CONSIGNMENT (KONSINYASI)

### SCENARIO 8.1: Terima Barang Konsinyasi dari Supplier

**Langkah:**
1. Menu: **Inventory → Operations → Receipts**
2. Klik: **Create**
3. Isi:

```
═══════════════════════════════════════════════════════
FORM GOODS RECEIPT
═══════════════════════════════════════════════════════

OPERATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Operation Type:     Receipts
Vendor:             PT Chemindo Maju (Consignment Supplier)

PRODUCTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌─────────────────────────────────────────────────────┐
│ Product:           Glycerin 99%                     │
│ Quantity:          100 kg                          │
│ Unit:              kg                              │
│ Unit Price:        45.000/kg                       │
│ Consignment:       ✅ Yes                          │
│ Lot/Serial:        LOT-CM-GLY-2026-09              │
└─────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════
```

4. Klik: **Save**
5. Klik: **Validate**

**Hasil:**
```
Receipt: WH/IN/xxxx
Status: Done
Location: Consignment - PT Chemindo Maju
Stock: 100 kg (consigned)
```

---

### SCENARIO 8.2: Pakai Barang Konsinyasi

**Langkah:**
1. Menu: **Inventory → Operations → Internal Transfers**
2. Klik: **Create**
3. Isi:

```
═══════════════════════════════════════════════════════
FORM INTERNAL TRANSFER
═══════════════════════════════════════════════════════

SOURCE & DESTINATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Source Location:     Consignment - PT Chemindo Maju
Destination:        Production

PRODUCTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌─────────────────────────────────────────────────────┐
│ Product:           Glycerin 99%                     │
│ Quantity:          30 kg          ← Dipakai         │
└─────────────────────────────────────────────────────┘

REASON
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reason:            Digunakan untuk MO/2026/09/0025
                   Batch Sabun Wajah GlowUp

═══════════════════════════════════════════════════════
```

4. Klik: **Validate**

**Hasil:**
```
Transfer: Internal/xxxx
Glycerin moved: Consignment → Production
Qty consumed: 30 kg
```

---

### SCENARIO 8.3: Monthly Reconciliation

**Langkah:**
1. Menu: **Inventory → Reporting**
2. Cari: **Consignment Reconciliation**

**Report:**
```
═══════════════════════════════════════════════════════
KONSINYASI RECONCILIATION
PT Chemindo Maju - September 2026
═══════════════════════════════════════════════════════

AWAL BULAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Opening Stock:      100 kg
Opening Value:       Rp 4.500.000

PENERIMAAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Received:            0 kg

PEMAKAIAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MO/2026/09/0020:    20 kg
MO/2026/09/0025:    30 kg
─────────────────────────────────────────────────────
Total Pemakaian:    50 kg

AKHIR BULAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Closing Stock:      50 kg
Closing Value:       Rp 2.250.000

INVOICE REQUIRED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Qty untuk diinvoice:    50 kg
Harga:                   Rp 45.000/kg
Total Invoice:           Rp 2.250.000

═══════════════════════════════════════════════════════
```

---

## CHECKLIST FINAL TESTING

### MODUL UTAMA
| No | Modul | Test | Status | Catatan |
|----|-------|------|--------|---------|
| 1 | Sales | Buat Quotation | ⬜ | |
| 2 | Sales | Konfirmasi SO | ⬜ | |
| 3 | Sales | Buat SO Distributor | ⬜ | |
| 4 | Purchase | Buat RFQ | ⬜ | |
| 5 | Purchase | Confirm PO | ⬜ | |
| 6 | Purchase | Terima Barang | ⬜ | |
| 7 | Inventory | Lihat Stock | ⬜ | |
| 8 | Inventory | Delivery Order | ⬜ | |
| 9 | Inventory | Reorder Point | ⬜ | |
| 10 | Manufacturing | Buat MO | ⬜ | |
| 11 | Manufacturing | Produce Done | ⬜ | |
| 12 | Manufacturing | Buat BoM | ⬜ | |
| 13 | Manufacturing | Cost Analysis | ⬜ | |
| 14 | QC | QC Approved | ⬜ | |
| 15 | QC | QC Rework | ⬜ | |
| 16 | QC | QC Rejected | ⬜ | |
| 17 | QC | QC Dashboard | ⬜ | |
| 18 | Regulatory | Product Registration | ⬜ | |
| 19 | Regulatory | Ingredient Monitor | ⬜ | |
| 20 | Consignment | Terima Consignment | ⬜ | |
| 21 | Consignment | Pakai Consignment | ⬜ | |
| 22 | Consignment | Reconciliation | ⬜ | |
| 23 | n8n | Login | ⬜ | |
| 24 | n8n | Test Lead Capture | ⬜ | |
| 25 | n8n | Cek Active Workflows | ⬜ | |

---

## BUGS & ISSUES

| No | Tanggal | Deskripsi | Severity | Status | Solusi |
|----|---------|-----------|----------|--------|--------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

---

## TANDA TANGAN

```
Tester: ___________________________
Tanggal: ___________________________
Disetujui oleh: ___________________________
```

