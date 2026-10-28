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

*Document Version: 1.1*
*Last Updated: 2026-09-12*

---

## ADDON BARU: FITUR TAMBAHAN

### 9. BoM SECURITY (Keamanan Formula)

#### Tujuan:
Melindungi rahasia formula produk dari staf produksi. Staf hanya melihat instruksi kerja dengan kode bahan, bukan nama bahan kimia.

#### Cara Pakai:

**A. Setup Material Code:**
1. Menu: `Inventory` → `Products`
2. Buka produk bahan baku
3. Tab: `BoM Security`
4. Isi:
   - `Material Code`: Kode unik (misal: K001, B002)
   - `Display Name Short`: Nama singkat untuk floor
   - `Confidential Material`: Aktifkan jika bahan perlu proteksi

**B. Setup Formula Security:**
1. Menu: `Manufacturing` → `Bill of Materials`
2. Buka BoM produk
3. Centang `Confidential Formula`
4. Isi `Formula Code` (misal: FRM/00001)

**C. Generate Work Instructions:**
1. Buka Manufacturing Order
2. Tab: `Work Instructions (Floor)`
3. Klik `Generate Instructions`
4. Instruksi menampilkan kode bahan, bukan nama asli

#### User Groups:
| Group | Akses |
|-------|-------|
| BoM: Production Staff (Restricted) | Kode bahan saja |
| BoM: R&D Admin (Full) | Nama bahan lengkap |
| BoM: QC Staff (Result) | Hasil jadi, bukan formula |

---

### 10. REGULATORY & BPOM TRACKING

#### Tujuan:
Track status dokumen BPOM dan Halal. Notifikasi WA otomatis ke klien saat status berubah.

#### Cara Pakai:

**A. Buat Project BPOM:**
1. Menu: `Regulatory` → `BPOM Projects`
2. Create → Isi:
   - Project Name: "BPOM Serum X - Client A"
   - Client: Pilih klien
   - Regulatory Type: BPOM Registration
   - Products: Pilih produk terkait

**B. Checklist Items:**
1. Buka project → Tab `Checklist`
2. Default checklist BPOM tersedia:
   - Prepare Formula Composition
   - Prepare Certificate of Analysis (CoA)
   - Stability Test Report
   - Microbial Challenge Test
   - Submit to BPOM
   - Receive Approval

**C. Update Status:**
1. Buka project
2. Field `Status`: Draft → Submitted → Under Review → Approved
3. Centang `Send WA Notification` → Notifikasi WA otomatis ke klien

#### Status BPOM:
| Status | Keterangan |
|--------|------------|
| Draft | Konsep dokumen |
| Submitted | Sudah submit ke BPOM |
| Under Review | Sedang direview BPOM |
| Pending Info | Butuh info tambahan |
| Approved | Disetujui |
| Rejected | Ditolak, perlu revisi |

---

### 11. CONSIGNMENT / TOLL MANUFACTURING

#### Tujuan:
Track inventory milik klien (packaging/cl) dengan valuation Rp0.

#### Cara Pakai:

**A. Setup Consignment Location:**
1. Menu: `Inventory` → `Configuration` → `Locations`
2. Create → `Consignment Location`: ✓
3. `Consignment Owner`: Pilih klien

**B. Setup Consignment Product:**
1. Menu: `Inventory` → `Products`
2. Create/Edit product
3. Tab `Consignment`:
   - `Consignment`: ✓
   - `Owner (Client)`: Pilih klien
   - `standard_price`: Otomatis = 0

**C. Receive Consignment Goods:**
1. Menu: `Inventory` → `Operations` → `Receipts`
2. Create → Pilih vendor (kosongkan atau klien)
3. Destination Location: WH/Consignment/[Nama Klien]
4. Validate

**D. Filter Consignment Moves:**
1. Menu: `Inventory` → `Reporting` → `Stock Moves`
2. Filter: `Consignment Moves`

---

### 12. N8N AUTOMATION ENDPOINTS

#### Webhook URLs:

| Workflow | Endpoint | Fungsi |
|----------|----------|--------|
| Lead Capture | `http://localhost:5678/webhook/lead` | Terima lead dari website |

#### Payload Format:
```json
{
  "name": "Nama Klien",
  "email": "email@klien.com",
  "phone": "628123456789",
  "product": "Sunscreen SPF 50",
  "quantity": "5000 pcs",
  "message": "Pesan inquiry"
}
```

#### Test Command:
```bash
curl -X POST http://localhost:5678/webhook/lead \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Client", "email": "test@test.com", "phone": "628123456789"}'
```

---

### 13. INSTALLED ADDONS

| Addon | Fungsi |
|-------|--------|
| duanaga_bom_security | BoM Security & formula protection |
| duanaga_regulatory | BPOM/Halal tracking |
| duanaga_consignment | Toll manufacturing & consignment |
| duanaga_qc_integration | QC KBR integration |
| duanaga_website | Website lead capture |

---

*Last Updated: 2026-09-12*
