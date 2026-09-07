# ERP PT DUA NAGA KOSMETINDO
## Panduan Penggunaan - Maklon Kosmetik

---

## AKSES SISTEM

- **URL:** http://localhost:8069
- **Database:** duanaga
- **Login:** admin / admin

---

## 1. ORDER BARU DARI KLIEN (SALES ORDER)

### Langkah:
1. **Menu:** `Sales` → `Orders` → `Create`
2. **Customer:** Pilih dari daftar (Beauty Glow, SkinLab, dll)
3. **Add Product:** Klik `Add a product` → pilih produk
4. **Quantity:** Masukkan jumlah (misal: 1000)
5. **Notes:** Tambah instruksi packaging
6. **Save** → `Confirm`

### Contoh Input:
```
Customer: Beauty Glow Indonesia
Product: Face Serum Vitamin C 30ml
Quantity: 1000 pcs
Unit Price: Rp 85.000
Notes: Private Label - Botol Custom + Box Logo
```

### Status Order:
- `Quotation` → Draft/Quote
- `Sent` → Sudah dikirim ke customer
- `Sale Order` → Confirm/Sudah locked
- `Done` → Selesai

---

## 2. PEMBELIAN BAHAN BAKI (PURCHASE ORDER)

### Langkah:
1. **Menu:** `Purchase` → `Orders` → `Create`
2. **Vendor:** Pilih supplier (CV Chemindo, PT Packpro, dll)
3. **Add Product:** Tambah bahan baku yang needed
4. **Quantity:** Masukkan jumlah sesuai kebutuhan
5. **Confirm** → `Confirm Order`

### Receiving (Terima Barang):
1. **Menu:** `Inventory` → `Operations` → `Receipts`
2. **Create** → Pilih PO yang sudah confirm
3. **Validate** → Barang masuk warehouse

### Contoh Input:
```
Vendor: CV Chemindo Sentosa
Products:
  - Vitamin C Powder: 50 kg @ Rp 500.000
  - Niacinamide: 20 kg @ Rp 420.000
  - Glycerin USP: 100 kg @ Rp 180.000
```

---

## 3. PRODUKSI (MANUFACTURING)

### Langkah:
1. **Menu:** `Manufacturing` → `Orders` → `Create`
2. **Product:** Pilih Finish Goods (Face Serum, Body Lotion, dll)
3. **Quantity:** Jumlah yang mau diproduksi
4. **BoM:** Otomatis terisi dari Bill of Materials
5. **Confirm** → `Confirm`

### Production Flow:
```
MO Created → In Progress → Done
                    ↓
           Finish Goods masuk
           WH/Stock/FG location
```

### Untuk Produce:
1. **Manufacturing** → Click MO
2. **Button:** `Produce` atau `Mark as Done`
3. **Consume:** Materials otomatis dikurangi dari stock
4. **Finish:** Products masuk ke warehouse

### Contoh:
```
Product: Face Serum Vitamin C 30ml
Quantity: 1000 pcs
BOM Components:
  - Vitamin C Powder: 0.5 kg
  - Glycerin: 1.0 kg
  - Niacinamide: 0.3 kg
```

---

## 4. PENGIRIMAN KE KLIEN (DELIVERY)

### Langkah:
1. **Menu:** `Inventory` → `Operations` → `Delivery Orders`
2. **Create** → Pilih SO yang mau dikirim
3. **Check:** Product + Quantity sesuai SO
4. **Validate** → Barang keluar warehouse

### Atau dari Sales Order:
1. **Sales** → Open SO
2. **Button:** `Delivery` → `Validate`
3. Stok langsung terupdate

---

## 5. R&D FORMULA (PROJECT)

### Langkah:
1. **Menu:** `Project` → Pilih project (R&D Skincare/Haircare)
2. **Create Task** → Tambah task baru
3. **Assign:** Ke team member
4. **Description:** Detail formula, trial notes

### Contoh Task:
```
Task: Formulasi Sunscreen SPF 60
Assigned to: R&D Team
Description:
- Target SPF: 60
- Water resistant: Ya
- Trial batch: 3
- Notes: Using SPF Booster Compound
```

---

## 6. STOCK OPERATION (LANGSUNG)

### Goods Receipt (Barang Masuk):
```
Menu: Inventory → Operations → Receipts
Create → Vendor: pilih → Add product → Validate
```

### Goods Issue (Barang Keluar):
```
Menu: Inventory → Operations → Delivery Orders
Create → Customer: pilih → Add product → Validate
```

### Internal Transfer:
```
Menu: Inventory → Operations → Internal Transfers
Move: WH/Stock/BB → WH/Produksi
```

---

## 7. LAPORAN

### Menu: `Reporting`

| Report | Fungsi |
|--------|--------|
| Inventory Valuation | Nilai stok saat ini |
| Stock Moves | Riwayat beweging barang |
| Sales Analysis | Analisis penjualan |
| Purchase Analysis | Analisis pembelian |
| MRP Analysis | Produksi report |

---

## 8. USER & ACCESS (ADMIN)

### Menu: `Settings` → `Users`

| User | Role |
|------|------|
| admin | Full Access |
| marketing@duanaga.co.id | Sales |
| produksi@duanaga.co.id | Manufacturing |
| purchasing@duanaga.co.id | Purchase |
| gudang@duanaga.co.id | Inventory |
| qc@duanaga.co.id | QC/Inventory |

Password default: `Duanaga2024`

---

## FLOW MAKLON LENGKAP

```
1. CLIENT ORDER
   Sales → Create SO → Confirm

2. PROCUREMENT
   Purchase → PO → Receive → Stock BB

3. PRODUCTION
   Manufacturing → MO → Produce → Finish Goods

4. QC CHECK
   Inventory → Quality → Check product

5. DELIVERY
   Delivery Order → Validate → Kirim ke Client

6. INVOICING
   Accounting → Customer Invoices → Create
```

---

## STRUKTUR PRODUK

### Kategori:
- **Kosmetik** (Parent)
  - Face Care
  - Body Care
  - Hair Care
  - Sunscreen
  - dll

### Tipe Product:
- **Storable (Product):** Finish Goods - tracking stock
- **Consumable (Consu):** Bahan Baku - tidak tracking stock detail
- **Service:** Jasa maklon

---

## WAREHOUSE STRUCTURE

```
WH: Dua Naga Main Warehouse
├── WH/Stock/BB      → Bahan Baku
├── WH/Stock/PK      → Packaging
├── WH/Stock/FG      → Finish Goods
├── WH/QC            → Quality Control
├── WH/Produksi      → Production Area
└── WH/Output        → Finished Products
```

---

## NOMOR DOKUMEN

| Document | Format |
|----------|--------|
| Sales Order | SO/2026/00001 |
| Purchase Order | PO/2026/00001 |
| Manufacturing | MO/2026/00001 |
| Delivery | DN/2026/00001 |
| Receipt | WH/2026/00001 |

---

## KONTAK

- **Email:** marketing@duanaga.co.id
- **Phone:** +62 811-2127-464
- **Website:** https://duanaga.co.id
- **Alamat:** Dk. Gambiran, Ds. Krajan, Kec. Gatak, Kab. Sukoharjo, Jawa Tengah 57557

---

*Document Version: 1.0*
*Last Updated: 2026-09-05*
